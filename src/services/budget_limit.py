import json
from ..constants import LIMITS_FILE
from ..helpers.date_utils import get_month_name
from ..services.expense_data import get_summary

def get_limit(limit_file, month):
    try:
        with open(limit_file, "r") as lmtfile:
            lmtfile.seek(0)
            content = lmtfile.read().strip()

            if not content:
                return []

            data = json.load(lmtfile)

            for limit in data:
                if limit["name"] == month:
                    return limit

            return []

    except Exception as e:
        print(e, "Error")

def limit_exists(limit_file, month):
    try:
        with open(limit_file, "r") as lmtfile:
            lmtfile.seek(0)
            content = lmtfile.read().strip()

            # if file is empty return False
            if not content:
                return False

            lmtfile.seek(0)
            data = json.load(lmtfile)
            for limit in data:
                if limit.get("name") == month:
                    print(
                        f"""
    There's already a budget for this month
    Month: {limit["name"]}
    Budget: {limit["amount"]}
    Spent this month: {limit["spentSoFar"]}
                """
                    )
                    return True

        return False

    except FileNotFoundError:
        with open(limit_file, "w", encoding="utf-8") as lmtfile:
            json.dump([], lmtfile, indent=4)
            return False

    except json.JSONDecodeError:
        print(f"Error: Json file '{limit_file}' is corrupted. Reinitializing.")
        with open(limit_file, "w", encoding="utf-8") as lmtfile:
            json.dump([], lmtfile, indent=4)
        return False

def add_limit(limit_file_name, new_budget):
    try:
        with open(limit_file_name, "r", encoding="utf-8") as lmtfile:
            content = lmtfile.read()
            if content:
                json_data = json.loads(content)
            else:
                json_data = []
    except FileNotFoundError:
        print(f"File {limit_file_name} not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file.")

    json_data.append(new_budget)

    with open(limit_file_name, "w", encoding="utf-8") as lmtfile:
        json.dump(json_data, lmtfile, indent=4, ensure_ascii=False)

    print(
        f"""
    New budget has been added.
    Month: {new_budget["name"]}
    Amount: {new_budget["amount"]}
    """
    )

# get_current_limit_data можно удалить, т.к. get_limit делает то же самое
def get_current_limit_data(limit_file_name, month):
    try:
        with open(limit_file_name, "r", encoding="utf-8") as lmtfile:
            content = lmtfile.read()
            if content:
                json_data = json.loads(content)
            else:
                return None

    except FileNotFoundError:
        print(f"No budget has been assigned at this time")
        return None
    except json.JSONDecoreError:
        print(f"Json error happened.")
        return None

    for limit in json_data:
        if limit.get("month") == month:
            return limit

def check_budget(limit_file_name):
    def decorator(func):
        def wrapper(filename, data, expense):
            date_obj = datetime.strptime(expense[1], "%Y-%m-%d")
            month_expense = get_month_name(date_obj.month)

            # START LOGIC

            if limit_exists(limit_file_name, month_expense):
                limit = get_limit(limit_file_name, month_expense)

            month_budget = limit["amount"]

            month_sum = get_summary(month_expense)

            if month_sum < month_budget:
                print("LESS")

        return wrapper

    return decorator