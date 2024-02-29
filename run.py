import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPE_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPE_CREDS)
SHEET = GSPREAD_CLIENT.open('budget_calculator')

income = SHEET.worksheet('income')
expenses = SHEET.worksheet('expenses')

income_data = income.get_all_values()
expenses_data = expenses.get_all_values()

def menu():
    print("Welcome to the Budget Calculator!\n")
    print("Please choose what you wish to do:\n")
    print("1. Add Income\n")
    print("2. Add an Expense\n")
    print("3. View Summary\n")

    choice = int(input("Select your choice:\n"))

    if choice == 1:
        print("1. Add Monthly Income\n")
        print("2. Add Additional Income\n")
        print("3. Exit\n")

        income_choice = int(input('Select your choice.\n'))

        if income_choice == 1:
            # add_monthly_income()
            pass
        elif income_choice == 2:
            # add_additional_income()
            pass
        else: income_choice == 3
            # menu()
    
    elif choice == 2:
        # add_expenses()
        pass
    
    elif choice == 3:
        print("1. View all Expenses by Month\n")
        print("2. View Monthly Expenses by Category\n")
        print("3. View Weekly Expenses\n")
        print("4. Monthly Summary\n")
        print("5. Yearly Summary\n")
        print("6. Exit\n")

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
            # view Yearly Summary
            pass
        else: view_choice == 6
            # exit
            # menu()
        
    else:
        print("Invalid choice, Please select: 1, 2 or 3.")

menu()

            