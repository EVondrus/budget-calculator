# Imports
import os
import gspread

from google.oauth2.service_account import Credentials
from datetime import datetime

# Define the scope required for accessing Google Sheets
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
# Load Google service account credentials from a JSON file
CREDS = Credentials.from_service_account_file('creds.json')
SCOPE_CREDS = CREDS.with_scopes(SCOPE)
# Authorize the Google Sheets API client
GSPREAD_CLIENT = gspread.authorize(SCOPE_CREDS)
# Open the Google Sheets document named 'budget_calculator'
SHEET = GSPREAD_CLIENT.open('budget_calculator')
# Access the 'income' and 'expenses' worksheets within the Google Sheets document
income = SHEET.worksheet('income')
expenses = SHEET.worksheet('expenses')
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
        print(f"You added {self.amount:.2f} to your Incomes")
        os.system('cls') 
        #menu()
        

def add_monthly_income():
    """
    Collects user input for monthly income and adds it to the Google Sheet "income".
    """
    # USER WANT TO INPUT THEIR OWN DATE MAYBE??
    date = datetime.now().strftime('%Y-%m-%d') 
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
                break # Exit the loop if the input is valid
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    new_income = IncomeEntry(date, description, amount)
    new_income.add_income_to_sheet(income)
    

def menu():
    """
    Display the menu and options to the user
    """
    while True: # Use a loop to keep the menu running
        os.system('cls') # Clear the terminal
        print("Welcome to the Budget Calculator!\n")
        print("Please choose what you wish to do:\n")
        print("1. Add an Income\n")
        print("2. Add an Expense\n")
        print("3. View Summary\n")
        print("4. Exit\n")

        choice = int(input("Select your choice:\n"))

        if choice == 1:
            print("1. Add Monthly Income\n")
            print("2. Add Additional Income\n")
            print("3. Back to Main Menu\n")

            income_choice = int(input('Select your choice.\n'))

            if income_choice == 1:
                add_monthly_income()
            elif income_choice == 2:
                # additional_income()
                pass
            elif income_choice == 3:
                continue # Go back to the main menu
    
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

            view_choice = int(input('Select your choice.\n'))

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
                continue # Go back to the main menu
    
        elif choice == 4:
            print("Exiting the Budget Calculator.")
            break # Exit the loop and the program
            
        
        else:
            print("Invalid choice, Please select: 1, 2, 3 or 4.")
        

    
menu()





            