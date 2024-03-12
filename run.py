# Imports
import os
import gspread
import time
import calendar

from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

if __name__ == "__main__":
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
        print(Fore.RED +
              f"An error occurred while accessing the Google Sheets API: {e}")
        print("Please check your internet connection and try again.")
        exit()

    # Access the 'income' and 'expenses' worksheets
    # within the Google Sheets document
    try:
        income = SHEET.worksheet("income")
        expenses = SHEET.worksheet("expenses")

    except gspread.exceptions.WorksheetNotFound:
        print(Fore.RED + "The specified worksheet could not be found.")
        exit()

    except gspread.exceptions.APIError as e:
        print(Fore.RED +
              f"An error occurred while accessing the worksheets: {e}")
        exit()

    # Retrieve all existing data from the 'income' and 'expenses' worksheets
    income_data = income.get_all_values()
    expenses_data = expenses.get_all_values()

    # Extract expense categories from the third column
    expense_categories = list(set([row[2] for row in expenses_data[1:]]))

    def print_slow(text):
        """
        Print each character of the text with a delay, including color codes.
        """
        # Slow down the printing of each character
        for char in text:
            print(char, end="", flush=True)
            time.sleep(0.1)

    def display_welcome_message():
        print(Fore.YELLOW + "\nWelcome to the Budget Calculator!\n")
        time.sleep(1)
        print(Fore.GREEN + "This application helps you track "
              "your income and expenses")
        print(Fore.GREEN + "providing insights into your financial health.\n")
        time.sleep(1.5)
        print("Please press Enter to continue.")
        input()
        os.system("clear")

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
                    print(Fore.YELLOW +
                          f"Please enter one of these numbers:{valid_choices}")
            except ValueError:
                print(Fore.RED + "Only numbers allowed!")
        os.system("clear")
        return user_input

    def add_category(category):
        """
        Adds a category to the list of expense categories.
        """
        global expense_categories

        # Add the category to the expense_categories list
        if category not in expense_categories:
            expense_categories.append(category)
            print(Fore.GREEN + f"Category '{category}' added successfully.\n")
            time.sleep(3)
            os.system("clear")

        else:
            print(Fore.RED + f"Category '{category}' already exists.")
            print("Please enter a new category name\n")

    def choose_category():
        """
        Displays a list of expense categories with numbers for selection.
        Allows the user to choose an existing category or create a new one.
        """
        global expense_categories

        # Loop until a valid category is chosen
        while True:
            print(Fore.YELLOW + "Select category by number:")

            # Print categories with numbers starting from 1
            for i, category in enumerate(expense_categories, start=1):
                print(f"{i}. {category}")

            # Add an option for the user to create a new category
            print(Fore.GREEN + f"{len(expense_categories) + 1}. "
                  "Create a new category\n")

            # Generate a list of valid choices (category numbers)
            # including the option for creating a new category
            # +2 to include the option for creating a new category
            valid_choices = list(range(1, len(expense_categories) + 2))

            # Use get_number_choice function to get the validated user's choice
            category_choice = get_number_choice(
                Fore.YELLOW + "Select your choice:\n",
                valid_choices
            )

            # If the user chose to create a new category
            # Check against the index of the new category option
            if category_choice == len(expense_categories) + 1:

                while True:
                    category = input(Fore.YELLOW + "Enter the name of "
                                     "the new category:\n")

                    # Check if the category already exists in the list
                    if category not in expense_categories:
                        # Call add_category to handle adding the category
                        add_category(category)
                        break
                    else:
                        print(Fore.RED + f"'{category}' already exists "
                              "in the list.\n")
                        print("Enter a new category or choose from the list.")
                break  # Exit the loop after adding a new category

            else:
                category = expense_categories[category_choice - 1]
                break  # Exit the loop if an existing category is selected

        return category

    class Entry:

        def __init__(self, date=None, description=None,
                     category=None, amount=None):
            """
            Initialize a new Entry object with
            specified date, description, category, and amount.
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
                    print_slow(Fore.GREEN + "Income added successfully!\n")
                    print(f"You added {self.amount:.2f} to your Incomes")

                elif entry_type == "expense":
                    print_slow(Fore.GREEN + "Expense added successfully!\n")
                    print(f"You spent {self.amount:.2f} on {self.description}")

            except gspread.exceptions.APIError as e:
                print(Fore.RED + "An error occurred:")
                print(Fore.RED + f"While interacting with "
                      "the Google Sheets API: {e}")
                print("Please check your internet connection and try again.")

            except Exception as e:
                print(Fore.RED + f"An unexpected error occurred: {e}")

            time.sleep(5)
            os.system("clear")

        def collect_data(self, is_additional=False, is_expense=False):
            """
            Collects user input for date, category, description, and amount.
            """
            today = datetime.now().strftime("%Y-%m-%d")
            print(Fore.YELLOW + f"Today's date is: {today}.")
            print(f"Press Enter to choose today's date or input a new date:\n")

            date = today
            # Input for Date, auto save on todays date with enter key
            while True:
                date_input = input("Date of entry (YYYY-MM-DD):\n")

                if not date_input:
                    print(Fore.GREEN + f"Automatically saved on "
                          "today's date: {today}\n")
                    break

                try:
                    datetime.strptime(date_input, "%Y-%m-%d")
                    date = date_input
                    break

                except ValueError:
                    print(Fore.RED + "Invalid date format!")
                    print("Please enter the date in YYYY-MM-DD format.")

            # Set Defaults for Description and Category for Income
            if not is_additional:
                self.description = "Monthly Income"
                self.category = "Monthly Income"
                # Print the description for monthly income
                print(Fore.GREEN + f"{self.category}\n")

            else:
                while True:
                    if is_additional and is_expense is False:
                        self.category = "Extra Income"
                        print(Fore.GREEN + f"{self.category}\n")

                    # User set Description and default Category
                    description = input(
                        "Enter description (max 12 characters):\n")
                    print()

                    if description.strip() == "":
                        print(Fore.RED +
                              "Description cannot be empty."
                              "Please enter a description.")

                    elif 1 <= len(description) <= 12:
                        self.description = description
                        break

                    else:
                        print(Fore.RED + "The description must be between"
                              "1 and 12 characters. Please try again.")

            while True:
                # Input Amount for Income and Expense
                try:
                    amount = float(input("Enter the amount (Post-Tax):\n"))
                    print()

                    if amount < 0:
                        print(Fore.RED + "Amount must be a positive number."
                              "Please try again.")
                    else:
                        break

                except ValueError:
                    print(Fore.RED + "Invalid input. Please enter a number.")

            self.date = date
            self.amount = amount

            os.system("clear")
            time.sleep(0.5)

    class IncomeEntry(Entry):

        def add_monthly_income(self, worksheet):
            """
            Adds monthly income with a fixed description ("Monthly Income").
            """
            self.collect_data(is_additional=False, is_expense=False)
            self.add_to_sheet(worksheet, "income", "Monthly Income")

        def add_additional_income(self, worksheet):
            """
            Collects user input for additional income
            including date, description, and amount,
            and adds it to the Google Sheet income".
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
        Prompts the user for a month and year, validates the input
        returns a tuple of start_date, end_date.
        """
        while True:
            try:
                month = int(input("Enter the month (MM): \n"))
                if not (1 <= month <= 12):
                    print(Fore.RED + "Invalid month. Please enter a "
                          "month between 01 and 12.")
                    continue

                year = int(input("Enter the year (YYYY): \n"))

                # Convert month and year to start_date
                start_date = datetime.strptime(
                    f"{year}-{month:02d}-01", "%Y-%m-%d")

                # Calculate the last day of the month
                # Which correctly handles leap years
                end_date = start_date.replace(
                    day=calendar.monthrange(year, month)[1])

                # Return start_date and end_date as a tuple
                return start_date, end_date

            except ValueError:
                print(Fore.RED + "Invalid input. "
                      "Please enter a valid month and/or year.")
            except TypeError:
                print(Fore.RED + "Invalid input type. "
                      "Please enter numbers for the month and year.")

    def get_weekly_date_input(self):
        """
        Prompts the user for a date, validates the input,
        and returns a tuple of start_date, end_date for the week.
        """
        while True:
            try:
                date_input = input(
                    Fore.YELLOW + "Please enter a date (YYYY-MM-DD): \n")
                selected_date = datetime.strptime(date_input, "%Y-%m-%d")
                # Calculate start and end dates of the week
                start_date = selected_date - timedelta(
                    days=selected_date.weekday())
                end_date = start_date + timedelta(days=6)
                return start_date, end_date

            except ValueError:
                print(Fore.RED + "Invalid date format."
                      "Please enter the date in the format YYYY-MM-DD.")
                continue

    def filter_expenses_by_date_range(self, start_date, end_date):
        """
        Filters expenses data based on a given date range.
        """
        return [
            row for row in self.expenses_data[1:]
            if (
                start_date <= datetime.strptime(row[0], "%Y-%m-%d") < end_date
            )
        ]

    def calculate_total_income(self, start_date, end_date):
        """
        Calculates the total income for a given date range.
        """
        total_income = 0
        for row in self.income_data[1:]:  # Skip the header row
            income_date = datetime.strptime(row[0], "%Y-%m-%d")
            if start_date <= income_date <= end_date:
                # Remove comma from amount string before converting to float
                # Bug solved:
                # https://docs.python.org/3/library/stdtypes.html#str.replace
                amount_str_wo_comma = row[3].replace(',', '')
                total_income += float(amount_str_wo_comma)

        return total_income

    def calculate_total_expenses(self, expenses):
        """
        Calculates the total expenses from a list of expenses.
        """
        return sum(float(expense[3]) for expense in expenses)

    def calculate_expenses_by_category(self, expenses):
        """
        Calculates the total expenses by category from a list of expenses.

        """
        expenses_by_category = {}

        for expense in expenses:
            # Category is in the third column
            category = expense[2]
            # Amount is in the fourth column
            amount = float(expense[3])
            if category in expenses_by_category:
                expenses_by_category[category] += amount
            else:
                expenses_by_category[category] = amount
        return expenses_by_category

    def calculate_remaining_income(self, total_income, total_expenses):
        """
        Calculates the remaining income after subtracting
        total expenses from total income.
        """
        remaining_income = total_income - total_expenses
        return remaining_income

    def view_expenses_by_category(self, start_date, end_date):
        """
        Displays the expenses by category for a given date range.
        """
        filtered_expenses = self.filter_expenses_by_date_range(
            start_date, end_date
        )
        expenses_by_category = self.calculate_expenses_by_category(
            filtered_expenses
        )

        # Convert the dictionary to a list of tuples for easier sorting
        expenses_list = list(expenses_by_category.items())

        # Sort the list by category name
        expenses_list.sort(key=lambda x: x[0])

        # Display the total expenses for each category in a list
        print(Fore.YELLOW + "\nExpenses by Category:\n")
        for category, total in expenses_list:
            print(f"{category}: {total:.2f}")

        time.sleep(15)
        os.system("clear")

    def view_monthly_expenses(self):
        """
        Allows the user to view all expenses for a
        chosen month and displays the total.
        """
        # Get start and end date from user input
        start_date, end_date = self.get_date_input()
        # Filter expenses by the chosen date range
        filtered_expenses = self.filter_expenses_by_date_range(
            start_date, end_date)
        # Calculate the total expenses for the selected month
        total_expenses = self.calculate_total_expenses(filtered_expenses)
        # Display the total expenses for the chosen month
        if filtered_expenses:
            print(f"\nTotal expenses for {start_date.strftime('%B %Y')}: "
                  f"{total_expenses:.2f}\n")
        else:
            print(
                Fore.RED + f"No expenses found for "
                "{start_date.strftime('%B %Y')}.")

        time.sleep(15)
        os.system("clear")

    def view_weekly_expenses(self):
        """
        Displays the total expenses for the week that includes a specific date,
        based on the calendar week, and the remaining income after expenses.
        """
        while True:
            try:
                # Get the specific date from user input
                start_date, end_date = self.get_weekly_date_input()

                # Calculate the week number of the year for the input date
                week_number = start_date.isocalendar()[1]

                # Filter expenses by the chosen date range
                filtered_expenses = self.filter_expenses_by_date_range(
                    start_date, end_date)

                if not filtered_expenses:
                    print(Fore.RED + f"No expenses found for week "
                          f"{week_number} of {start_date.year}, "
                          f"from: {start_date.strftime('%Y-%m-%d')} "
                          f"to: {end_date.strftime('%Y-%m-%d')}.\n")
                    continue  # loop to prompt for a new date

                # Calculate total expenses for the selected week
                total_expenses = self.calculate_total_expenses(
                    filtered_expenses)

                # Calculate the total income
                total_income = self.calculate_total_income(
                    start_date, end_date)

                # Calculate remaining income after expenses
                remaining_income = self.calculate_remaining_income(
                    total_income, total_expenses)

                os.system("clear")

                # Display the total expenses for the chosen week
                # including the week number
                print(Fore.YELLOW + "\nWeekly Expenses\n")
                print(f"Week: {week_number} of {start_date.year}")
                print(f"From: {start_date.strftime('%Y-%m-%d')} to "
                      f"{end_date.strftime('%Y-%m-%d')}")
                print(f"Total Expenses: {total_expenses:.2f}\n")
                print(Fore.YELLOW + f"Remaining Income After Expenses: "
                      f"{remaining_income:.2f}\n")

                break  # Exit the loop if expenses are found and displayed

            except ValueError as e:
                print(Fore.RED + f"An error occurred while processing "
                      "the date: {e}")
                continue
            except Exception as e:
                print(Fore.RED + f"An unexpected error occurred: {e}")
                break  # Exit the loop if an unexpected error occurs

        time.sleep(15)
        os.system("clear")

    def view_monthly_summary(self):
        """
        Displays the total income, total expenses
        and remaining income for a given month.
        """
        # Get start and end date from user input
        start_date, end_date = self.get_date_input()

        # Calculate the total income for the selected month
        total_income = self.calculate_total_income(start_date, end_date)

        # Filter expenses by the chosen date range
        filtered_expenses = self.filter_expenses_by_date_range(
            start_date, end_date)

        # Calculate total expenses for the selected month
        total_expenses = self.calculate_total_expenses(filtered_expenses)

        # Calculate remaining income after expenses
        remaining_income = self.calculate_remaining_income(
            total_income, total_expenses)

        os.system("clear")

        print(Fore.YELLOW + "\nMonthly Summary\n")
        print(f"Month: {start_date.strftime('%B %Y')}\n")
        print(f"Total Income: {total_income:.2f}\n")
        print(f"Total Expenses: {total_expenses:.2f}\n")
        print(Fore.YELLOW + f"Remaining Income: {remaining_income:.2f}\n")

        time.sleep(15)
        os.system("clear")

    def view_yearly_summary(self):
        """
        Displays the total income, total expenses
        and remaining income for a given year.
        """
        # Get the year from user input
        year = input("Enter the year (YYYY): \n")

        # Convert the year to start_date and end_date for the entire year
        start_date = datetime.strptime(f"{year}-01-01", "%Y-%m-%d")
        end_date = datetime.strptime(f"{year}-12-31", "%Y-%m-%d")

        # Calculate the total income for the selected year
        total_income = self.calculate_total_income(start_date, end_date)

        # Filter expenses by the chosen date range
        filtered_expenses = self.filter_expenses_by_date_range(
            start_date, end_date)

        # Calculate total expenses for the selected year
        total_expenses = self.calculate_total_expenses(filtered_expenses)

        # Calculate remaining income after expenses
        remaining_income = self.calculate_remaining_income(
            total_income, total_expenses)

        os.system("clear")

        print(Fore.YELLOW + "\nYearly Summary\n")
        print(f"Year: {year}\n")
        print(f"Total Income: {total_income:.2f}\n")
        print(f"Total Expenses: {total_expenses:.2f}\n")
        print(Fore.YELLOW + f"Remaining Income: {remaining_income:.2f}\n")

        time.sleep(15)
        os.system("clear")


# Instance of the Summary class with the loaded data
summary = Summary(expenses_data, income_data)


def menu():
    """
    Display the menu and options to the user
    """
    while True:  # Use a loop to keep the menu running
        print(Fore.YELLOW + "Please choose what you wish to do:\n")
        print("1. Add an Income\n")
        print("2. Add an Expense\n")
        print("3. View Summary\n")
        print("4. Exit\n")

        choice = get_number_choice(
            "Select your choice:\n", [1, 2, 3, 4]
        )

        if choice == 1:
            print("1. Add Monthly Income\n")
            print("2. Add Additional Income\n")
            print("3. Back to Main Menu\n")

            income_choice = get_number_choice(
                "Select your choice:\n", [1, 2, 3]
            )

            if income_choice == 1:
                income_entry_instance = IncomeEntry()
                income_entry_instance.add_monthly_income(income)

            elif income_choice == 2:
                income_entry_instance = IncomeEntry()
                income_entry_instance.add_additional_income(income)

            elif income_choice == 3:
                continue  # Go back to the beginning of the menu loop

        elif choice == 2:
            print("1. Add Expense\n")
            print("2. Back to Main Menu\n")

            expense_choice = get_number_choice(
                "Select your choice:\n", [1, 2]
            )

            if expense_choice == 1:
                expense_entry_instance = ExpenseEntry()
                expense_entry_instance.add_expense(expenses)

            elif expense_choice == 2:
                continue  # Go back to the beginning of the menu loop

        elif choice == 3:
            print("1. View all Expenses by Month\n")
            print("2. View Monthly Expenses by Category\n")
            print("3. View Weekly Expenses\n")
            print("4. Monthly Summary\n")
            print("5. Yearly Summary\n")
            print("6. Back to Main Menu\n")

            view_choice = get_number_choice(
                "Select your choice:\n", [1, 2, 3, 4, 5, 6]
            )

            if view_choice == 1:
                summary.view_monthly_expenses()

            elif view_choice == 2:
                start_date, end_date = summary.get_date_input()
                summary.view_expenses_by_category(start_date, end_date)

            elif view_choice == 3:
                summary.view_weekly_expenses()
            elif view_choice == 4:
                summary.view_monthly_summary()
            elif view_choice == 5:
                summary.view_yearly_summary()
            elif view_choice == 6:
                continue  # Go back to the beginning of the menu loop

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


if __name__ == "__main__":
    try:
        display_welcome_message()
        menu()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    exit()
