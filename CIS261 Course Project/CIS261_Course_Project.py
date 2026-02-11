#Elijah Figaro
#CIS 261
#CIS 261 Course Project

from datetime import datetime
from pathlib import Path
from typing import Tuple, Dict


DEFAULT_DATA_FILE = Path("employees.txt")

def get_employee_name() -> str:
    return input("Enter employee name (or 'end' to finish): ").strip()

def get_dates_and_hours() -> Tuple[str, str, float]:
    """Input and return from_date, to_date, and hours_worked."""
    from_date = input("Enter from date (mm/dd/yyyy): ").strip()
    to_date = input("Enter to date (mm/dd/yyyy): ").strip()
    hours_worked = float(input("Enter hours worked: ").strip())
    return from_date, to_date, hours_worked

def calculate_pay(hours: float, rate: float, tax_rate: float) -> Tuple[float, float, float]:
    gross_pay = hours * rate
    income_tax = gross_pay * tax_rate
    net_pay = gross_pay - income_tax
    return gross_pay, income_tax, net_pay

def resolve_data_file(preferred: Path = DEFAULT_DATA_FILE) -> Path:
    """
    Ensure we have a writable data file path.
    Try preferred first. If permission denied, fall back to the user's Documents folder.
    """
    try:
     
        with open(preferred, "a", encoding="utf-8"):
            pass
        return preferred
    except PermissionError:
        fallback = Path.home() / "Documents" / "employees.txt"
        try:
            fallback.parent.mkdir(parents=True, exist_ok=True)
            with open(fallback, "a", encoding="utf-8"):
                pass
            print(f"Warning: cannot write to '{preferred}'. Using fallback file: '{fallback}'.")
            return fallback
        except PermissionError:
            print(f"Error: permission denied writing to both '{preferred}' and '{fallback}'.")
            raise

def write_record_to_file(from_date: str, to_date: str, name: str,
                         hours: float, rate: float, tax_rate: float,
                         filename: Path = None) -> None:
    """Append a pipe-delimited record to the data file. Handles permission errors."""
    if filename is None:
        filename = resolve_data_file()
    record = f"{from_date}|{to_date}|{name}|{hours}|{rate}|{tax_rate}\n"
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(record)
    except PermissionError:
        
        alt = resolve_data_file(Path.home() / "Documents" / "employees.txt")
        with open(alt, "a", encoding="utf-8") as f:
            f.write(record)

def prompt_report_from_date() -> str:
    """Ask user for report start From Date or 'All'. Validate mm/dd/yyyy format when not 'All'."""
    while True:
        user_input = input("Enter From Date for report (mm/dd/yyyy) or 'All' to show all records: ").strip()
        if user_input.lower() == "all":
            return "All"
        try:
            datetime.strptime(user_input, "%m/%d/%Y")
            return user_input
        except ValueError:
            print("Invalid date format. Please enter date as mm/dd/yyyy or type 'All'.")

def read_records_and_generate_report(request_from_date: str,
                                     filename: Path = None) -> None:
    """Read pipe-delimited records from file, compute pay for matching records and display totals."""
    if filename is None:
        try:
            filename = resolve_data_file()
        except PermissionError:
          
            filename = DEFAULT_DATA_FILE

    totals: Dict[str, float] = {
        "employees": 0,
        "hours": 0.0,
        "gross": 0.0,
        "tax": 0.0,
        "net": 0.0
    }

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"No data file found ({filename}). No records to display.")
        return
    except PermissionError:
        print(f"Permission denied reading file '{filename}'. Unable to generate report.")
        return

    for line in lines:
        parts = line.split("|")
        if len(parts) != 6:
         
            continue
        rec_from, rec_to, rec_name, rec_hours, rec_rate, rec_tax = parts
       
        if request_from_date != "All" and rec_from != request_from_date:
            continue
        try:
            hours = float(rec_hours)
            rate = float(rec_rate)
            tax_rate = float(rec_tax)
        except ValueError:
           
            continue

        gross, income_tax, net = calculate_pay(hours, rate, tax_rate)

        print("\nEmployee Summary")
        print(f"Name: {rec_name}")
        print(f"From Date: {rec_from}")
        print(f"To Date: {rec_to}")
        print(f"Hours Worked: {hours}")
        print(f"Hourly Rate: ${rate:.2f}")
        print(f"Gross Pay: ${gross:.2f}")
        print(f"Tax Rate: {tax_rate:.2%}")
        print(f"Income Tax: ${income_tax:.2f}")
        print(f"Net Pay: ${net:.2f}")

        totals["employees"] += 1
        totals["hours"] += hours
        totals["gross"] += gross
        totals["tax"] += income_tax
        totals["net"] += net

    
    print("\n===== TOTALS =====")
    print(f"Total Employees: {int(totals['employees'])}")
    print(f"Total Hours Worked: {totals['hours']}")
    print(f"Total Gross Pay: ${totals['gross']:.2f}")
    print(f"Total Income Tax: ${totals['tax']:.2f}")
    print(f"Total Net Pay: ${totals['net']:.2f}")

def main() -> None:
    print("Employee data entry. Records will be appended to the data file.")
    while True:
        name = get_employee_name()
        if name.lower() == "end":
            break

        from_date, to_date, hours_worked = get_dates_and_hours()
        hourly_rate = float(input("Enter hourly rate: ").strip())
        tax_rate = float(input("Enter income tax rate (e.g., 0.20 for 20%): ").strip())

        write_record_to_file(from_date, to_date, name, hours_worked, hourly_rate, tax_rate)


    report_from = prompt_report_from_date()
    read_records_and_generate_report(report_from)

if __name__ == "__main__":
    main()
