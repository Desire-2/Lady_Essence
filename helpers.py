from datetime import datetime, timedelta

def calculate_cycle_dates(last_period_date, cycle_length):
    """
    Calculate the key dates for a menstrual cycle based on the last period date and cycle length.

    Args:
        last_period_date (str): The last period date in the format "DD/MM/YYYY".
        cycle_length (int): The length of the cycle in days.

    Returns:
        tuple: A tuple containing next period date, ovulation date, fertile start, and fertile end dates.
    """
    try:
        last_date = datetime.strptime(last_period_date, "%d/%m/%Y")
        next_period = last_date + timedelta(days=cycle_length)
        ovulation = last_date + timedelta(days=cycle_length - 14)
        fertile_start = ovulation - timedelta(days=5)
        fertile_end = ovulation + timedelta(days=1)
        return next_period, ovulation, fertile_start, fertile_end
    except ValueError:
        raise ValueError("Invalid date format. Please use DD/MM/YYYY.")
