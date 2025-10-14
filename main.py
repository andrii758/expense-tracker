import csv
import time
import sys
import os


csv_fields = ['ID', 'Date', 'Description', 'Amount']
FILENAME = "expense.csv"

def add_expense(desc, amount):
    # нужно прикрутить айди когда пойму как будут загружаться и выгружаться данные
    return ['ID', f'{time.ctime(time.time)}', desc, amount]
    
def create_file():
    with open(FILENAME, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_fields)
        print("Fields were added successfully.")

def main():
    if not os.path.exists(FILENAME) and os.path.getsize(FILENAME) != 0:
        create_file()

if __name__ == "__main__":
    main()
