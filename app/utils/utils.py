from datetime import datetime, date
import os


def verify_date(date_str):
    try:
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
        today = date.today()
        return parsed_date.date() >= today
    except ValueError:
        return False


def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Created directory: {directory_path}")
