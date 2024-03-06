# The Budget Calculator
The Budget Calculator provides a simple yet effective solution for managing personal finances. With its intuitive interface and seamless integration with Google Sheets, users can easily track their income and expenses, enabling better financial decision-making.

The live link can be found here - [Budget Calculator]()

![Flowchart]()

## Site Owner Goals
- Provide users with a functional and user-friendly application for managing their finances efficiently.
- Encourage users to return to the application regularly by offering valuable features and insights into their financial activities.
- Foster trust and reliability by ensuring accurate data management and secure handling of sensitive financial information.

## User Stories

- ### As a user I want to:
 - Understand the main purpose of the budget calculator and how it can help manage my finances effectively.
 - Be guided through the process of adding income and expenses, ensuring that the interface is intuitive and easy to navigate.
 - Have access to a summary of my budgeting activities, including total income, total expenses, total expenses by category and remaining balance.


## Logic Flow
To visualize the sequence of actions needed in the budget calculator, I utilized Lucid Chart to create a flowchart. This approach proved invaluable as it enabled me to conceptualize the project's structure, delineate necessary functions, and understand the interaction among various components.



As the flow chart was created at the outset of the project, it does not fully reflect all elements of the game.

![Flow Chart]()

## Features

### Title and Introduction Section
- 
- 

![Welcome]()

### Interactive Menu:

The program features an interactive menu that guides users through different options:
- The menu is chosen by numbers.
1. Adding income 
2. Adding expenses.
3. Viewing summaries.
4. Exit the program.

![User Menu]()

### Adding income Entries:
- The user can choose between adding an Monthly income or Additional income.
- Users adds their monthly income with a fixed description ("Monthly Income") and a default category ("Monthly Income").
- Additional income entries allow users to input a custom description with a default category ("Extra Income").
- The program collects data such as the date, description, default category and amount of the income entry.

### Adding Expense Entries:

- Users can add expenses with  costum details including the date, category, description, and amount.
- The program allows users to choose existing expense categories or create new ones as needed.

### Viewing Summary:

Users can view various summaries to track their budget:
1. View all expenses by month.
2. View monthly expenses by category.
3. View weekly expenses.
4. View monthly and yearly summaries of income and expenses.

### Date Handling:

- The program displays today's date by default.
- Users have the option to press Enter to automatically insert today's date for income and expense entries.
- Users can also choose to input their own date for income and expenses if preferred.

### Data Management:

- Utilizes Google Sheets API for storing income and expense data.
- Implements error handling to manage unexpected inputs or errors during execution.

### Security:

- Utilizes Google OAuth2 authentication for secure access to Google Sheets.
- Ensures that sensitive data is handled securely and only authorized users can access the budget data.

### Input Validation and Error Handling
The following input validation is carried out on the user input:
- Length Check:
    - Income/Expense descriptions and expense categories must not exceed 12 characters.
    - To ensure clarity in the Google sheets and consistency, descriptions are limited.

- Numeric Entry:
    - Amounts entered for income and expenses must be positive numbers.
    - The system prompts users to re-enter values if they input negative numbers or non-numeric characters, ensuring accurate financial data.

- Menu and Category Selection:
    - When adding expenses, users must select a category from the provided list or create a new one.
    - If the user does not input a number option when navigating in the menues, they will get an error message asking them to input a valid option.

- Date Input:
    - If the user enters a date in an incorrect format, the program detects the deviation.
    - A clear error message informs the user about the invalid format and prompts them to enter the date again in correct format.

![Input Validation]()
- Exit function:
    - Users are prompted to input either 'y' or 'n' to confirm their choice to exit the program
    - The program distinguishes between lowercase and uppercase letters, accepting only lowercase input.
    - If the user chooses to quit, a goodbye message appears and the calculator is ended using the `exit()` method.

![Goodbye]()


### Summary 
- Google Sheets serves as the central repository for storing and retrieving financial data. The budget calculator accesses Google Sheets via the Google Drive and Google Sheets APIs hosted on the Google Cloud Platform.

![Google Sheet]()

- To ensure secure access to Google Sheets, dedicated credentials were generated and stored. These credentials are securely managed within the cred.json file, included in the .gitignore to prevent inadvertent exposure on GitHub. 
- Additionally, they are configured as environment variables (Config Vars) on Heroku, ensuring secure access during runtime.
- This integration of Google Sheets enhances the functionality of the budget calculator, providing users with a robust platform for managing and analyzing their financial data effectively.
- PANDAS FOR SORTING?

![]()

