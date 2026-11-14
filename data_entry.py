# Collect data from the user

from datetime import datetime


# Date format used throughout the program
date_format = "%d-%m-%Y"


# Categories used in the finance tracker
# I = Income
# E = Expense
CATEGORIES = {
    "I": "Income",
    "E": "Expense"
}


def get_date(prompt, allow_default=False):

    # Ask the user to enter a date
    date_str = input(prompt)


    # If default is allowed and the user presses Enter,
    # use today's date
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)


    try:

        # Convert the entered text into a date
        valid_date = datetime.strptime(
            date_str,
            date_format
        )

        # Convert the date back into the required format
        return valid_date.strftime(date_format)


    except ValueError:

        # Show an error if the date format is incorrect
        print(
            "Invalid date format. "
            "Please enter the date in dd-mm-yyyy format"
        )

        # Ask the user for the date again
        return get_date(prompt, allow_default)



def get_amount():

    try:

        # Ask the user to enter the transaction amount
        amount = float(
            input("Enter the amount: ")
        )


        # Amount must be greater than zero
        if amount <= 0:
            raise ValueError(
                "Amount must be a non-negative non-zero value."
            )


        # Return the valid amount
        return amount


    except ValueError as e:

        # Display the error message
        print(e)

        # Ask the user for the amount again
        return get_amount()



def get_category():

    # Ask the user to enter I or E
    category = input(
        "Enter the category "
        "('I' for Income or 'E' for Expense): "
    ).upper()


    # Check whether the entered category is valid
    if category in CATEGORIES:
        return CATEGORIES[category]


    # Show an error for an invalid category
    print(
        "Invalid category. "
        "Please enter 'I' for Income or 'E' for Expense."
    )


    # Ask the user again
    return get_category()



def get_description():

    # Ask the user for a description
    # The description can be left empty
    return input(
        "Enter a description (optional): "
    )


# -------------For Own Purposes--------------------- 
#get_date() -> Gets and validates the transaction date
#get_amount() -> Gets and validates the amount
#get_category() -> Gets Income or Expense
#get_description() -> Gets the transaction description
