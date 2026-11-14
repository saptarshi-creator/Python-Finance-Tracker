# Main flow of the finance tracker
import pandas as pd
import csv
import matplotlib.pyplot as plt
from datetime import datetime

# Import functions used to take input from the user
from data_entry import get_amount, get_category, get_date, get_description



class CSV:
    # Name of the CSV file where transactions are stored
    CSV_FILE = "finance_data.csv"

    # Column names used in the CSV file
    COLUMNS = ["date", "amount", "category", "description"]

    # Date format used throughout the program
    FORMAT = "%d-%m-%Y"



    @classmethod 
    def initialize_csv(cls):
        # Check whether the CSV file already exists
        try:
            pd.read_csv(cls.CSV_FILE)


        # If the file does not exist, create a new empty CSV file
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)



    @classmethod
    def add_entry(cls, date, amount, category, description):
        # Create a dictionary containing the new transaction

        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }

        # Open the CSV file in append mode and add the new transaction
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS) 
            writer.writerow(new_entry)

        print("Entry Added Successfully")


    @classmethod
    def get_transactions(cls, start_date, end_date):

        # Read all transactions from the CSV file
        df = pd.read_csv(cls.CSV_FILE)

        # Convert the date column from text into datetime objects
        df["date"] = pd.to_datetime(
            df["date"], format=CSV.FORMAT)

        # Convert the user-entered dates into datetime objects
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        # Select only transactions within the selected date range
        mask = (
            (df["date"] >= start_date) & (df["date"] <= end_date)
        )

        filtered_df = df.loc[mask]


        # Check whether any transactions were found
        if filtered_df.empty:
            print('No transactions found in the given data range')

        else:
            print(
                f"Transaction from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}"
                )
            
            # Display the filtered transactions
            print(filtered_df.to_string(
                   index=False,
                    formatters={
                        "date": lambda x: x.strftime(CSV.FORMAT)}
                )
            )

            # Calculate total income
            total_income = (
                filtered_df[
                    filtered_df["category"] == "Income"
                    ]["amount"].sum()
            )

            # Calculate total expenses
            total_expense = (
                filtered_df[
                    filtered_df["category"] == "Expense"
                    ]["amount"].sum()
            )


            # Calculate and display the financial summary
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")

        # Return the filtered transactions
        return filtered_df


def add():
    # Make sure the CSV file exists before adding data
    CSV.initialize_csv()

    # Get transaction date from the user
    date = get_date(
        "Enter the date of transaction (dd-mm-yyyy) or enter for today's date: ",
        allow_default=True
    )

    # Get amount, category and description from the user
    amount = get_amount()
    category = get_category()
    description = get_description()

    # Save the transaction to the CSV file
    CSV.add_entry(
                date,
                amount,
                category,
                description
                )


def plot_transaction(df):

    # Ask the user whether they want a daily or monthly graph
    choice = input(
        "\nWhat type of graph do you want?\n"
        "1. Daily\n"
        "2. Monthly\n"
        "Enter your choice: "
    )

    # Use the date column as the index
    # This is required for resampling by day or month
    df = df.set_index("date")

    if choice == "1":

        # ---------------- DAILY GRAPH ---------------

        # Calculate total income for each day
        income_df = (
            df[df["category"] == "Income"]
            .resample("D")["amount"]
            .sum()
        )

        # Calculate total expenses for each day
        expense_df = (
            df[df["category"] == "Expense"]
            .resample("D")["amount"]
            .sum()
        )

        # Create a continuous date range
        # This also includes days with no transactions
        all_dates = pd.date_range(
            start=df.index.min(),
            end=df.index.max(),
            freq="D"
        )

        # Fill missing days with 0
        income_df = income_df.reindex(
            all_dates,
            fill_value=0
        )

        
        expense_df = expense_df.reindex(
            all_dates,
            fill_value=0
        )

        # Calculate net savings for each day
        savings_df = income_df - expense_df

        # Create the graph
        plt.figure(figsize=(12, 6))

        # Plot daily income
        plt.plot(
            all_dates,
            income_df,
            label="Income",
            color="green"
        )

        # Plot daily expenses
        plt.plot(
            all_dates,
            expense_df,
            label="Expense",
            color="red"
        )

        # Plot daily net savings
        plt.plot(
            all_dates,
            savings_df,
            label="Net Savings",
            color="blue"
        )

        # Add labels and title
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.title("Daily Income, Expense and Net Savings")

        # Show the legend and grid
        plt.legend()
        plt.grid(True)

        # Rotate dates so they are easier to read
        plt.xticks(rotation=45)

        # Adjust the graph layout
        plt.tight_layout()

        # Display the graph
        plt.show()


    elif choice == "2":

        # ---------------- MONTHLY GRAPH ----------------

        # Calculate total income for each month
        income_df = (
            df[df["category"] == "Income"]
            .resample("ME")["amount"]
            .sum()
        )

        # Calculate total expenses for each month
        expense_df = (
            df[df["category"] == "Expense"]
            .resample("ME")["amount"]
            .sum()
        )

        # Calculate net savings for each month
        savings_df = income_df - expense_df

        # Create the graph
        plt.figure(figsize=(12, 6))

        # Plot monthly income
        plt.plot(
            income_df.index,
            income_df,
            label="Income",
            color="green",
            marker="o"
        )

        # Plot monthly expenses
        plt.plot(
            expense_df.index,
            expense_df,
            label="Expense",
            color="red",
            marker="o"
        )

        # Plot monthly net savings
        plt.plot(
            savings_df.index,
            savings_df,
            label="Net Savings",
            color="blue",
            marker="o"
        )

         # Add labels and title
        plt.xlabel("Month")
        plt.ylabel("Amount")
        plt.title("Monthly Income, Expense and Net Savings")

        # Show the legend and grid
        plt.legend()
        plt.grid(True)

        # Rotate month labels
        plt.xticks(rotation=45)

        # Adjust the graph layout
        plt.tight_layout()

        # Display the graph
        plt.show()

    else:
        # Handle an invalid graph choice
        print("Invalid choice. Please select 1 or 2.")




def main():

    # Keep showing the menu until the user chooses Exit
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")


        if choice == "1":
            # Add a new transaction
            add()

        elif choice == "2":
          
           # Ask the user for the date range
          start_date = get_date(
              "Enter the start date (dd-mm-yyyy): "
            )

          end_date = get_date(
              "Enter the end date (dd-mm-yyyy): "
            )

           # Get transactions within the selected range
          df = CSV.get_transactions(
              start_date,
              end_date
        )

          # Only offer the graph if transactions were found
          if not df.empty:

            if input(
                "Do you want to see a plot? (y/n) "
            ).lower() == "y":
              
              # Display the graph menu
              plot_transaction(df)


        elif choice == "3":
            # Exit the program
            print("Exiting...")
            break

        else:
            # Handle an invalid menu choice
            print("Invalid choice . Enter 1, 2, or 3.")


# Start the program
if __name__ == "__main__":
    main()
