#Elijah Figaro
#CIS 261
#CIS 261 Course Project

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Tuple, Dict, List
import sys

# Default data file (attempt current working directory first).
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
        # Try opening in append mode to verify writability (file will be created if missing).
        with open(preferred, "a", encoding="utf-8"):
            pass
        return preferred
    except PermissionError:
        fallback = Path.home() / "Documents" / preferred.name
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
        # Try to resolve alternate file and retry once
        alt = resolve_data_file(Path.home() / "Documents" / (filename.name if filename else "employees.txt"))
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
            # If resolve_data_file raised, there's no writable file path — still attempt to read default if exists
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
            # skip malformed records
            continue
        rec_from, rec_to, rec_name, rec_hours, rec_rate, rec_tax = parts
        # If request is not All, only process matching From Date records
        if request_from_date != "All" and rec_from != request_from_date:
            continue
        try:
            hours = float(rec_hours)
            rate = float(rec_rate)
            tax_rate = float(rec_tax)
        except ValueError:
            # skip records with bad numeric data
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

    # Display totals after loop terminates
    print("\n===== TOTALS =====")
    print(f"Total Employees: {int(totals['employees'])}")
    print(f"Total Hours Worked: {totals['hours']}")
    print(f"Total Gross Pay: ${totals['gross']:.2f}")
    print(f"Total Income Tax: ${totals['tax']:.2f}")
    print(f"Total Net Pay: ${totals['net']:.2f}")

# -----------------------
# USER ACCOUNT / LOGIN ADD-ON
# -----------------------
USER_DATA_FILE = Path("users.txt")

@dataclass
class Login:
    user_id: str
    password: str
    authorization: str  # "Admin" or "User"

def load_existing_user_ids(filename: Path) -> List[str]:
    """Open the file in append mode (creates if missing), read existing records, return a list of user IDs."""
    user_ids: List[str] = []
    with open(filename, "a+", encoding="utf-8") as f:
        f.seek(0)
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if parts:
                user_ids.append(parts[0])
    return user_ids

def append_user_record(filename: Path, user_id: str, password: str, authorization: str) -> None:
    """Append a pipe-delimited user record to the file."""
    record = f"{user_id}|{password}|{authorization}\n"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(record)

def collect_user_entries(existing_ids: List[str], filename: Path) -> List[Login]:
    """
    Loop asking for new user entries until the user types 'End'.
    Validates duplicate User IDs and that authorization is 'Admin' or 'User'.
    Returns a list of newly created Login objects.
    """
    new_logins: List[Login] = []
    print("Enter new users. Type 'End' for User ID to finish.")
    while True:
        user_id = input("User ID: ").strip()
        if user_id.lower() == "end":
            break
        if not user_id:
            print("User ID cannot be empty.")
            continue
        if user_id in existing_ids:
            print("That User ID already exists. Choose a different User ID.")
            continue

        password = input("Password: ").strip()
        if not password:
            print("Password cannot be empty.")
            continue

        auth_input = input("Authorization code (Admin or User): ").strip()
        auth_norm = auth_input.capitalize()
        if auth_norm not in ("Admin", "User"):
            print("Invalid authorization. Must be 'Admin' or 'User'.")
            continue

        # Create Login object, persist to file, and update lists
        login_obj = Login(user_id, password, auth_norm)
        append_user_record(filename, user_id, password, auth_norm)
        existing_ids.append(user_id)
        new_logins.append(login_obj)
        print(f"Added user '{user_id}' with authorization '{auth_norm}'.")
    return new_logins

def display_login_list(logins: List[Login]) -> None:
    """Display user records from an in-memory list of Login objects."""
    if not logins:
        print("No user records to display.")
        return
    print("\nStored user records (in-memory):")
    for l in logins:
        print(f"User ID: {l.user_id} | Password: {l.password} | Authorization: {l.authorization}")

def display_all_user_records(filename: Path) -> None:
    """Read the file and display all stored User IDs, Passwords, and Authorization codes."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
    except FileNotFoundError:
        print(f"No user data file found ({filename}). Nothing to display.")
        return
    except PermissionError:
        print(f"Permission denied reading file '{filename}'. Unable to display records.")
        return

    if not lines:
        print("No user records stored.")
        return

    print("\nStored user records:")
    for line in lines:
        parts = line.split("|")
        if len(parts) != 3:
            continue
        user_id, password, authorization = parts
        print(f"User ID: {user_id} | Password: {password} | Authorization: {authorization}")

def load_all_logins(filename: Path) -> List[Login]:
    """Read all user records and return list of Login objects."""
    logins: List[Login] = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) != 3:
                    continue
                uid, pwd, auth = parts
                logins.append(Login(uid, pwd, auth.capitalize()))
    except FileNotFoundError:
        pass
    return logins

def login_prompt(filename: Path) -> Login:
    """Prompt for login, validate against stored records, return Login object on success or exit on failure."""
    logins = load_all_logins(filename)
    if not logins:
        print("No user accounts present. Please create at least one Admin account first.")
        # bootstrap: allow creation of at least one account
        ids = load_existing_user_ids(filename)
        collect_user_entries(ids, filename)
        logins = load_all_logins(filename)
        if not logins:
            print("No accounts created. Exiting.")
            sys.exit(1)

    user_id = input("Enter User ID: ").strip()
    password = input("Enter Password: ").strip()

    matching = [l for l in logins if l.user_id == user_id]
    if not matching:
        print("Error: User ID does not exist.")
        sys.exit(1)
    user_record = matching[0]
    if user_record.password != password:
        print("Error: Incorrect password.")
        sys.exit(1)

    # Successful login - return a Login object populated with stored data
    return Login(user_record.user_id, user_record.password, user_record.authorization)

def compute_user_totals(filename: Path) -> Tuple[int, int, int]:
    """Return totals: (total_users, admin_count, user_count)."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
    except (FileNotFoundError, PermissionError):
        return 0, 0, 0
    total = 0
    admin = 0
    user = 0
    for line in lines:
        parts = line.split("|")
        if len(parts) != 3:
            continue
        total += 1
        if parts[2].capitalize() == "Admin":
            admin += 1
        elif parts[2].capitalize() == "User":
            user += 1
    return total, admin, user

def user_account_flow() -> Login:
    """Bootstrap users if needed, then prompt login and return the logged-in Login object."""
    user_file = resolve_data_file(USER_DATA_FILE)
    existing_ids = load_existing_user_ids(user_file)

    # If no users exist, ask to bootstrap initial accounts
    if not existing_ids:
        print("No user accounts found. Create initial accounts (at least one Admin).")
        collect_user_entries(existing_ids, user_file)

    # Login
    current = login_prompt(user_file)
    print(f"Login successful. Authorization: {current.authorization}")
    return current

# -----------------------
# MAIN
# -----------------------
def main() -> None:
    # Run account/login flow first and obtain current user
    current = user_account_flow()

    # After login, continue to the employee entry/reporting and user-management steps
    if current.authorization.capitalize() == "Admin":
        # Admin: allow entering employee records then reporting
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

        # Admin user management after employee work
        user_file = resolve_data_file(USER_DATA_FILE)
        existing_ids = load_existing_user_ids(user_file)
        new_logins = collect_user_entries(existing_ids, user_file)
        # display from file and in-memory list for rubric
        display_all_user_records(user_file)
        display_login_list(load_all_logins(user_file))
        total, admin_count, user_count = compute_user_totals(user_file)
        print("\n===== USER TOTALS =====")
        print(f"Total Users: {total} | Admin: {admin_count} | User: {user_count}")

    else:
        # Standard user: skip entering employee data, run reporting only
        print("You are a standard user. Employee entry is not permitted; proceeding to reporting.")
        report_from = prompt_report_from_date()
        read_records_and_generate_report(report_from)

        # show user records (read-only)
        user_file = resolve_data_file(USER_DATA_FILE)
        display_all_user_records(user_file)
        total, admin_count, user_count = compute_user_totals(user_file)
        print("\nNote: You do not have permission to add users.")
        print("\n===== USER TOTALS (read-only) =====")
        print(f"Total Users: {total}")
        print(f"Admin Users: {admin_count}")
        print(f"Standard Users: {user_count}")

    print("\nProgram complete. Exiting.")

if __name__ == "__main__":
    main()

