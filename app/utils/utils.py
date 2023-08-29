from datetime import datetime, date

output_directory = "csv"

def verify_date(date_str):
    try:
        parsed_date = datetime.strptime(date_str, '%Y-%m-%d')
        today = date.today()
        if parsed_date.date() >= today:
            return True
        else:
            return False
    except ValueError:
        return False



