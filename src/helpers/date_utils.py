from datetime import datetime
import calendar


def get_month_boundaries(month_number: int, year: int = None):
    if year is None:
        year = datetime.now().year

    try:
        target_date = datetime(year, month_number, 1)
    except ValueError:
        raise ValueError("Invalid month number. Use numbers from 1 to 12.")

    start_of_month = target_date
    _, num_days_in_month = calendar.monthrange(year, month_number)
    end_of_month = target_date.replace(day=num_days_in_month)
    date_format = "%Y-%m-%d"

    start_date_str = start_of_month.strftime(date_format)
    end_date_str = end_of_month.strftime(date_format)

    return start_date_str, end_date_str


def get_month_name(month):
    month_map = {
        "1": "January",
        "01": "January",
        "january": "January",
        "2": "February",
        "02": "February",
        "february": "February",
        "3": "March",
        "03": "March",
        "march": "March",
        "4": "April",
        "04": "April",
        "april": "April",
        "5": "May",
        "05": "May",
        "may": "May",
        "6": "June",
        "06": "June",
        "june": "June",
        "7": "July",
        "07": "July",
        "july": "July",
        "8": "August",
        "08": "August",
        "august": "August",
        "9": "September",
        "09": "September",
        "september": "September",
        "10": "October",
        "october": "October",
        "11": "November",
        "november": "November",
        "12": "December",
        "december": "December",
    }
    key = str(month).strip().lower()
    if key in month_map:
        return month_map[key]
    else:
        raise ValueError("Invalid month input")


def get_month_number(month):
    month = month.capitalize()
    months = {
        "January": "01",
        "February": "02",
        "March": "03",
        "April": "04",
        "May": "05",
        "June": "06",
        "July": "07",
        "August": "08",
        "September": "09",
        "October": "10",
        "November": "11",
        "December": "12",
    }

    if isinstance(month, str):
        month = month.strip()

    if month.isdigit():
        month_number = int(month)
        if 1 <= month_number <= 12:
            return f"{month_number:02d}"
        else:
            raise ValueError("The month number must be between 1 and 12")

    elif month in months:
        return months[month]

    else:
        raise ValueError("Incorrect month entry")
