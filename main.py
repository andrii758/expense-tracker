import argparse
import csv
from datetime import datetime
import os
from tabulate import tabulate


FILENAME = "expense.csv"
FIELDS = ["ID", "Datetime", "Description", "Amount"]

def get_month_name(month):
    month_map = {
    '1': "January", '01': "January", "january": "January",
    '2': "February", '02': "February", "february": "February",
    '3': "March", '03': "March", "march": "March",
    '4': "April", '04': "April", "april": "April",
    '5': "May", '05': "May", "may": "May",
    '6': "June", '06': "June", "june": "June",
    '7': "July", '07': "July", "july": "July",
    '8': "August", '08': "August", "august": "August",
    '9': "September", '09': "September", "september": "September",
    '10': "October", "october": "October",
    '11': "November", "november": "November",
    '12': "December", "december": "December"
    }
    key = str(month).strip().lower()
    if key in month_map:
        return month_map[key]
    else:
        raise ValueError("Invalid month input")

def get_month_number(month):
    month = month.capitalize()
    months = {
            'January' : '01',
            'February' : '02',
            'March' : '03',
            'April' : '04',
            'May' : '05',
            'June' : '06',
            'July' : '07',
            'August' : '08',
            'September' : '09',
            'October' : '10',
            'November' : '11',
            'December' : '12'
            }
    
    if isinstance(month, str):
        month = month.strip()

    if month.isdigit():
        month_number = int(month)
        if 1 <= month_number <= 12:
            return f"{month_number:02d}"
        else:
            raise ValueError("The month number must be beetwen 1 and 12")

    elif month in months:
        return months[month]

    else:
        raise ValueError("Incorrect month entry")


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

def add_data(filename: str, data: list, expense: list):
    data.append(expense) 
    with open(filename, 'w', encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(data)
    print(f"Expense added successfully (ID : {expense[0]})")

def update_description(filename, ID, description):
    x = list(load_data(filename))
    for task in x:
        if task[0] == ID:
            task[2] = description
    write_data(filename, x)
    print("Description updated successfully")

def update_amount(filename, ID, amount):
    x = list(load_data(filename))
    for task in x:
        if task[0] == ID:
            task[3] = amount
    write_data(filename, x)
    print("Amount updated successfully")

def list_expenses(data):
    print(tabulate(data, headers="firstrow", tablefmt="fancy_grid"))

def get_summary(data, month=None):
    summary = 0 
    if month:
        for expense in data[1:]:
            if expense[1][5:7] == month:
                summary += float(expense[3])
    else:
        for expense in data[1:]:
            summary += float(expense[3])
    return summary

def delete_expense(data, ID):
    for expense in data[1:]:
        if expense[0] == ID:
            data.remove(expense)
    write_data(FILENAME, data)
    print(f"Expense deleted successfully (Description: {expense[2]})")

def main():
    # --- CREATE PARSER ---
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
    
    # --- LIST ---
    list_parser = subparsers.add_parser('list', help='List all expenses')

    # --- SUMMARY ---
    summary_parser = subparsers.add_parser('summary', help='Summary')
    summary_parser.add_argument('--month', help="To summary in a certain month")

    # --- DELETE ---
    delete_parser = subparsers.add_parser('delete', help="Delete an expense")
    delete_parser.add_argument('--id', help="Expense ID to delete")

    args = parser.parse_args()
    
    # --- LOAD DATA ---
    data = load_data(FILENAME)

    match args.command:
        case 'add':
            add_data(
                    FILENAME,
                    data, 
                    [len(data), 
                     datetime.now().strftime("%Y-%m-%d"), 
                     " ".join(args.description), 
                     args.amount
                     ]
                    )

        case 'update':
            if args.description:
                update_description(FILENAME, args.id, " ".join(args.description))
            if args.amount:
                update_amount(FILENAME, args.id, args.amount)
        case 'list':
            list_expenses(load_data(FILENAME))
        case 'summary':
            if args.month:
                print(f'Total expenses for {get_month_name(args.month)}: ${get_summary(data=load_data(FILENAME), month=get_month_number(args.month))}')
            else:
                print(f'Total expenses: ${get_summary(data=load_data(FILENAME))}')
        case 'delete':
            if args.id:
                delete_expense(load_data(FILENAME), args.id)
            else:
                print("Enter the ID using --id <expense id>")
        case _:
            print("No match found.")



if __name__ == "__main__":
    main()


