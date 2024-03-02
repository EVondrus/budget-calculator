# Imports
import os
import gspread

from google.oauth2.service_account import Credentials
from datetime import datetime

# Define the scope required for accessing Google Sheets
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]
# Load Google service account credentials from a JSON file
CREDS = Credentials.from_service_account_file("creds.json")
SCOPE_CREDS = CREDS.with_scopes(SCOPE)
# Authorize the Google Sheets API client
GSPREAD_CLIENT = gspread.authorize(SCOPE_CREDS)
# Open the Google Sheets document named 'budget_calculator'
SHEET = GSPREAD_CLIENT.open("budget_calculator")
# Access the 'income' and 'expenses' worksheets within the Google Sheets document
income = SHEET.worksheet("income")
expenses = SHEET.worksheet("expenses")
# Retrieve all existing data from the 'income' and 'expenses' worksheets
income_data = income.get_all_values()
expenses_data = expenses.get_all_values()


class IncomeEntry:
    """
    Initialize a new IncomeEntry object with specified date, description, and amount.
    """

    def __init__(self, date, description, amount):
        self.date = date
        self.description = description
        self.amount = amount

    def add_income_to_sheet(self, worksheet):
        """
        Adds a new row to the worksheet with income details.
        """
        next_row = len(worksheet.col_values(1)) + 1
        income_data = [self.date, self.description, self.amount]
        worksheet.insert_row(income_data, index=next_row)
        print("Income added successfully!")
        print(f"You added {self.amount:.2f} to your Income")


def add_monthly_income():
    """
    Collects user input for monthly income, Date, Description, Amount and adds it to the Google Sheet "income".
    """
    # Display today's date as the default option
    today = datetime.now().strftime("%Y-%m-%d")
    print(
        f"Today's date is {today}.\nPress Enter to choose todays date or Enter a different date:\n"
    )

    # Initialize date with today's date as the default
    date = today

    while True:
        # Prompt the user to enter a date, with the option to just press Enter for today's date
        user_input = input("Date of income (YYYY-MM-DD):\n")

        # If the user doesn't enter a date, use today's date
        if not user_input:
            print(f"Your income is automatically saved on todays date: {today}")
            break  # Exit the loop if the user presses Enter without typing a date

        # Validate the date format if the user enters a date
        try:
            datetime.strptime(user_input, "%Y-%m-%d")
            date = user_input  # Update the date if the format is valid
            break  # Exit the loop if the date is valid
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

    # Collect and validate description
    while True:
        description = input("Enter Income description (max 15 characters): \n")
        if len(description) > 15:
            print("The description must be 15 characters or less. Please try again.")
        else:
            break

    # Collect and validate amount
    while True:
        try:
            amount = float(input("Enter your Monthly Income (Post-Tax):\n"))
            if amount < 0:
                print("Amount must be a positive number. Please try again.")
            else:
                break  # Exit the loop if the input is valid
        except ValueError:
            print("Invalid input. Please enter a number.")

    new_income = IncomeEntry(date, description, amount)
    new_income.add_income_to_sheet(income)


def get_number_choice(input_title, valid_choices):
    """ 
    Function to validate User number input
    """
    input_is_valid = False
    while input_is_valid is False:
        user_input = input(input_title)
        try:
            user_input = int(user_input)
            if user_input in valid_choices:
                input_is_valid = True
            else:
                print(f"Please enter one of this numbers: {valid_choices}")
        except:
            print("Only numbers allowed")
    os.system("clear")
    return user_input


def menu():
    """
    Display the menu and options to the user
    """
    while True:  # Use a loop to keep the menu running
        print("Welcome to the Budget Calculator!\n")
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

            income_choice = get_number_choice("Select your choice:\n", [1, 2, 3])
            if income_choice == 1:
                add_monthly_income()
            elif income_choice == 2:
                # additional_income()
                pass
            elif income_choice == 3:
                continue  # Go back to the main menu

        elif choice == 2:
            # add_expenses()
            pass
        
        elif choice == 3:
            print("1. View all Expenses by Month\n")
            print("2. View Monthly Expenses by Category\n")
            print("3. View Weekly Expenses\n")
            print("4. Monthly Summary\n")
            print("5. Yearly Summary\n")
            print("6. Back to Main Menu\n")

            view_choice = get_number_choice("Select your choice:\n", [1, 2, 3, 4, 5, 6])
            if view_choice == 1:
                # view_all_expenses()
                pass
            elif view_choice == 2:
                # view_expenses_categories()
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
                confirm_exit = input("Are you sure you want to exit? (y / n):\n")
                if confirm_exit.lower() == "y":
                    print("Exiting the Budget Calculator.")
                    exit()  # Exit the loop and the program
                elif confirm_exit.lower() == "n":
                    break  # Exit the loop and go back to the main menu
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")

        else:
            print("Invalid choice, Please select: 1, 2, 3 or 4.")


menu()
