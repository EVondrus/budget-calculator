# Imports
import os
import gspread
import time

from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta

# Define the scope required for accessing Google Sheets
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]
# Load Google service account credentials from a JSON file
CREDS = Credentials.from_service_account_file("creds.json")
SCOPE_CREDS = CREDS.with_scopes(SCOPE)

try:
    # Authorize the Google Sheets API client
    GSPREAD_CLIENT = gspread.authorize(SCOPE_CREDS)
    # Open the Google Sheets document named 'budget_calculator'
    SHEET = GSPREAD_CLIENT.open("budget_calculator")
except gspread.exceptions.APIError as e:
    print(f"An error occurred while accessing the Google Sheets API: {e}")
    exit()

# Access the 'income' and 'expenses' worksheets within the Google Sheets document
try:
    income = SHEET.worksheet("income")
    expenses = SHEET.worksheet("expenses")
except gspread.exceptions.WorksheetNotFound:
    print("The specified worksheet could not be found.")
    exit()
except gspread.exceptions.APIError as e:
    print(f"An error occurred while accessing the worksheets: {e}")
    exit()

# Retrieve all existing data from the 'income' and 'expenses' worksheets
income_data = income.get_all_values()
expenses_data = expenses.get_all_values()

# Extract expense categories from the third column
expense_categories = list(set([row[2] for row in expenses_data[1:]]))


def get_number_choice(input_title, valid_choices):
    """
    Function to validate User number input
    """
    input_is_valid = False
    while not input_is_valid:
        user_input = input(input_title)
        try:
            user_input = int(user_input)
            if user_input in valid_choices:
                input_is_valid = True
            else:
                print(f"Please enter one of these numbers: {valid_choices}")
        except ValueError:
            print("Only numbers allowed")
    os.system("clear")
    return user_input


def print_slow(text):
    """
    Print each character of the text with a delay.
    """
    for char in text:
        print(char, end="", flush=True)
        # time.sleep(0.1)


def add_category(category):
    """
    Adds a category to the global list of expense categories.
    """
    global expense_categories
    # Add the category to the expense_categories list
    if category not in expense_categories:
        expense_categories.append(category)
        print(f"Category '{category}' added successfully.\n")
    else:
        print(f"Category '{category}' already exists.")


def choose_category():
    """
    Displays a list of expense categories with numbers for selection.
    Allows the user to choose an existing category or create a new one.
    """
    global expense_categories
    while True:  # Loop until a valid category is chosen
        # Print categories with numbers starting from 1
        print("Select category by number:")
        for i, category in enumerate(expense_categories, start=1):
            print(f"{i}. {category}")
        # Add an option for the user to create a new category
        print(f"{len(expense_categories) + 1}. Create a new category\n")
        # Generate a list of valid choices (category numbers) including the option for creating a new category
        # +2 to include the option for creating a new category
        valid_choices = list(range(1, len(expense_categories) + 2))
        # Use get_number_choice function to get the validated user's choice
        category_choice = get_number_choice(
            "Select your choice:\n", valid_choices)
        # If the user chose to create a new category
        # Check against the index of the new category option
        if category_choice == len(expense_categories) + 1:
            while True:
                category = input("Enter the name of the new category:\n")
                # Check if the category already exists in the list before adding it
                if category not in expense_categories:
                    # Call add_category function to handle adding the category
                    add_category(category)
                    break  # Exit the loop after adding a new category
                else:
                    print(f"Category: '{category}' already exists in the list.\nPlease enter a new Category name or choose from the list.")
            break  # Exit the loop after adding a new category
        else:
            category = expense_categories[category_choice - 1]
            break  # Exit the loop if an existing category is selected

    return category


class Entry:
    """
    Initialize a new IncomeEntry object with specified date, description, and amount.
    """

    def __init__(self, date=None, description=None, category=None, amount=None):
        """
        Initialize a new Entry object with specified date, description, category, and amount.
        """
        self.date = date
        self.description = description
        self.category = category
        self.amount = amount

    def add_to_sheet(self, worksheet, entry_type, category):
        """
        Adds a new row to the worksheet with details.
        """
        next_row = len(worksheet.col_values(1)) + 1
        income_data = [self.date, self.description, category, self.amount]
        try:
            worksheet.insert_row(income_data, index=next_row)
            if entry_type == "income":
                print_slow("Income added successfully!\n")
                print(f"You added {self.amount:.2f} to your Incomes")
            elif entry_type == "expense":
                print_slow("Expense added successfully!\n")
                print(f"You spent {self.amount:.2f} on {self.description}")
        except gspread.exceptions.APIError as e:
            print(f"An error occurred while interacting with the Google Sheets API: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        time.sleep(5)
        os.system("clear")

    def collect_data(self, is_additional=False, is_expense=False):
        """
        Collects user input for date, category, description, and amount.
        """
        today = datetime.now().strftime("%Y-%m-%d")
        print(f"Today's date is {today}.\nPress Enter to choose today's date or Enter a different date:\n")
        date = today
        # Input for Date
        while True:
            date_input = input("Date of entry (YYYY-MM-DD):\n")
            if not date_input:
                print(f"The new entry is automatically saved on today's date: {today}\n")
                break
            try:
                datetime.strptime(user_input, "%Y-%m-%d")
                date = date_input
                break
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

        # Set Defaults for Description and Category for Income
        if not is_additional:
            self.description = "Monthly Income"
            self.category = "Monthly Income"
            # Print the description for monthly income
            print(f"{self.description}\n")
        else:
            while True:
                # User set Description and default Category
                description = input("Enter description (max 12 characters):\n")
                print()
                if description.strip() == "":
                    print("Description cannot be empty. Please enter a description.")
                elif 1 <= len(description) <= 12:
                    self.description = description
                    self.category = "Extra Income"
                    break
                else:
                    print("The description must be between 1 and 12 characters. Please try again.")

        while True:
            # Input Amount for Income and Expense
            try:
                amount = float(input("Enter the amount (Post-Tax):\n"))
                print()
                if amount < 0:
                    print("Amount must be a positive number. Please try again.")
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a number.")

        self.date = date
        self.amount = amount


class IncomeEntry(Entry):
    def add_monthly_income(self, worksheet):
        """
        Adds monthly income with a fixed description ("Monthly Income").
        """
        self.collect_data(is_additional=False, is_expense=False)
        self.add_to_sheet(worksheet, "income", "Monthly Income")

    def add_additional_income(self, worksheet):
        """
        Collects user input for additional income, including date, description, and amount,
        and adds it to the Google Sheet "income".
        """
        self.collect_data(is_additional=True, is_expense=False)
        self.add_to_sheet(worksheet, "income", "Extra Income")

class ExpenseEntry(Entry):
    def add_expense(self, worksheet):
        self.collect_data(is_additional=True, is_expense=True)
        self.category = choose_category()
        self.add_to_sheet(worksheet, "expense", self.category)


class Summary:
    def __init__(self, expenses_data, income_data):
        self.expenses_data = expenses_data
        self.income_data = income_data

    def get_date_input(self):
        """
        Prompts the user for a month and year, validates the input, and returns a tuple of (start_date, end_date).
        """
        while True:
            # Prompt the user to input month
            month = input("Enter the month (MM): \n")
            if not (1 <= int(month) <= 12):
                print("Invalid month. Please enter a month between 01 and 12.")
                continue
            # Prompt the user to input year
            year = input("Enter the year (YYYY): \n")
            try:
                # Convert month and year to start_date
                start_date = datetime.strptime(
                    f"{year}-{month}-01", "%Y-%m-%d")
                # Calculate end_date assuming 31 days in a month
                end_date = start_date + timedelta(days=31)
                # Return start_date and end_date as a tuple
                return start_date, end_date
            except ValueError:
                print("Invalid year. Please try again.")
                continue

    def filter_expenses_by_date_range(self, start_date, end_date):
        """
        Filters expenses data based on a given date range.
        """
        # Iterate through each row in the expenses data and filter based on date range
        return [row for row in self.expenses_data[1:]
                if start_date <= datetime.strptime(row[0], "%Y-%m-%d") < end_date]

    def view_expenses_by_month(self):
        """
        Allows the user to view all expenses for a chosen month and displays the total.
        """
        # Get start and end date from user input
        start_date, end_date = self.get_date_input()
        # Filter expenses by the chosen date range
        filtered_expenses = self.filter_expenses_by_date_range(
            start_date, end_date)
        # Calculate the total expenses for the selected month
        total_expenses = sum(float(expense[3])
                             for expense in filtered_expenses)
        # Display the total expenses for the chosen month
        if filtered_expenses:
            print(f"\nTotal expenses for {
                  start_date.strftime('%m/%Y')}: {total_expenses:.2f}\n")
        else:
            print(f"No expenses found for {start_date.strftime('%m/%Y')}.")

        time.sleep(5)
        os.system("clear")

# Create an instance of the Summary class with the loaded data
summary = Summary(expenses_data, income_data)


def menu():
    """
    Display the menu and options to the user
    """
    while True:  # Use a loop to keep the menu running
        print_slow("Welcome to the Budget Calculator!\n\n")
        print("Please choose what you wish to do:\n")
        print("1. Add an Income\n")
        print("2. Add an Expense\n")
        print("3. View Summary\n")
        print("4. Exit\n")

        choice = get_number_choice("Select your choice:\n", [1, 2, 3, 4])
        if choice == 1:
            print("1. Add Monthly Income\n")
            print("2. Add Additional Income\n")
            print("3. Back to Main Menu\n")

            income_choice = get_number_choice(
                "Select your choice:\n", [1, 2, 3])
            if income_choice == 1:
                income_entry_instance = IncomeEntry()
                income_entry_instance.add_monthly_income(income)

            elif income_choice == 2:
                # Create an instance of IncomeEntry to call add_additional_income
                income_entry_instance = IncomeEntry()
                income_entry_instance.add_additional_income(income)

            elif income_choice == 3:
                continue  # Go back to the main menu

        elif choice == 2:
            print("1. Add Expense\n")
            print("2. Back to Main Menu\n")

            expense_choice = get_number_choice("Select your choice:\n", [1, 2])

            if expense_choice == 1:
                expense_entry_instance = ExpenseEntry()
                expense_entry_instance.add_expense(expenses)

            elif expense_choice == 2:
                continue

        elif choice == 3:
            print("1. View all Expenses by Month\n")
            print("2. View Monthly Expenses by Category\n")
            print("3. View Weekly Expenses\n")
            print("4. Monthly Summary\n")
            print("5. Yearly Summary\n")
            print("6. Back to Main Menu\n")

            view_choice = get_number_choice(
                "Select your choice:\n", [1, 2, 3, 4, 5, 6])
            if view_choice == 1:
                summary.view_expenses_by_month()
                pass
            elif view_choice == 2:
                # view_monthly_expenses_categories()
                pass
            elif view_choice == 3:
                # view_weekly_expenses()
                pass
            elif view_choice == 4:
                # view Monthly Summary
                pass
            elif view_choice == 5:
                #    view Yearly Summary
                pass
            elif view_choice == 6:
                continue  # Go back to the main menu

        elif choice == 4:
            while True:
                confirm_exit = input(
                    "Are you sure you want to exit? (y / n):\n")
                if confirm_exit.lower() == "y":
                    print("Exiting the Budget Calculator.")
                    exit()  # Exit the loop and the program
                elif confirm_exit.lower() == "n":
                    break  # Exit the loop and go back to the main menu
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")

        else:
            print("Invalid choice, Please select: 1, 2, 3 or 4.")


try:
    menu()
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit()