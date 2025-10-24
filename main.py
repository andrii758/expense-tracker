import argparse
import csv
from datetime import datetime
import os


FILENAME = "expense.csv"
FIELDS = ["ID", "Datetime", "Description", "Amount"]

def write_data(filename: str, data: list):
    with open(filename, 'w', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(data)
    print("File is rewritten.")


def load_data(filename: str):
    data = []
    if os.path.exists(filename) and os.path.getsize(filename) != 0:
        with open(filename, 'r') as csvfile:
           csvreader = csv.reader(csvfile)
           for row in csvreader:
              data.append(row)
    else:
        with open(filename, 'w', encoding='utf-8') as file:
            pass
        data = [['ID', 'Date' , 'Description', 'Amount']]
    
    return data

def add_data(filename: str, expense: list):
    x = list(load_data(filename))
    x.append(expense) 
    with open(filename, 'w', encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(x)
    print(f"Expense added successfully (ID : {expense[0]})")

def update_expense(filename, expense):
    x = list(load_data(filename))
    
#  тут нужно написать логику изменения описания либо суммы с помощью айди.
#  пока не понимаю как это сделать.

    write_data(filename, x)
    print("Expense updated successfully")

def main():
    parser = argparse.ArgumentParser(description="Expense tracker CLI application.")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # --- ADD ---
    add_parser = subparsers.add_parser('add', help="Add an expense")
    add_parser.add_argument('-d', '--description', nargs="+", help="Description")
    add_parser.add_argument('-a', '--amount', help="Amount")

    # --- UPDATE ---
    update_parser = subparsers.add_parser('update', help='Update an existing expense')
    update_parser.add_argument('--id', help="Expense ID")
    update_parser.add_argument('-d', '--description', nargs="+", help="Update descripion")
    update_parser.add_argument('-a', '--amount', help="Update amount")

    args = parser.parse_args()
    
    # --- LOAD DATA ---
    data = load_data(FILENAME)

    print(args.command, args.description, args.amount)
    print(args)
    match args.command:
        case 'add':
            add_data(
                    FILENAME, 
                    [len(data), 
                     datetime.now().strftime("%Y-%m-%d"), 
                     " ".join(args.description), 
                     args.amount
                     ]
                    )

        case 'update':
            update_expense(
                    FILENAME,
                    [args.id,
                     " ".join(args.description),
                     args.amount]
                    )
        case _:
            print("No match found.")



if __name__ == "__main__":
    main()


