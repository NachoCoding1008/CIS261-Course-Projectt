#Elijah Figaro
#CIS 261
#CIS 261 Course Project

def get_employee_name():
    return input("Enter employee name (or 'end' to finish): ")

def get_dates_and_hours():
    """Input and return from_date, to_date, and hours_worked."""
    from_date = input("Enter from date (mm/dd/yyyy): ")
    to_date = input("Enter to date (mm/dd/yyyy): ")
    hours_worked = float(input("Enter hours worked: "))
    return from_date, to_date, hours_worked

def calculate_pay(hours, rate, tax_rate):
    gross_pay = hours * rate
    income_tax = gross_pay * tax_rate
    net_pay = gross_pay - income_tax
    return gross_pay, income_tax, net_pay

def process_employees(employees, totals):
    """
    employees: list of lists -> [name, from_date, to_date, hours, rate, tax_rate]
    totals: dictionary to accumulate totals
    Calculates gross/tax/net, displays each employee summary (including dates),
    and increments totals in the totals dictionary.
    """
    for emp in employees:
        name, from_date, to_date, hours, rate, tax_rate = emp
        gross_pay, income_tax, net_pay = calculate_pay(hours, rate, tax_rate)

       
        print("\nEmployee Summary")
        print(f"Name: {name}")
        print(f"From Date: {from_date}")
        print(f"To Date: {to_date}")
        print(f"Hours Worked: {hours}")
        print(f"Hourly Rate: ${rate:.2f}")
        print(f"Gross Pay: ${gross_pay:.2f}")
        print(f"Tax Rate: {tax_rate:.2%}")
        print(f"Income Tax: ${income_tax:.2f}")
        print(f"Net Pay: ${net_pay:.2f}")

        
        totals["employees"] += 1
        totals["hours"] += hours
        totals["gross"] += gross_pay
        totals["tax"] += income_tax
        totals["net"] += net_pay

def display_totals(totals):
    """Read totals from the dictionary and display formatted totals."""
    print("\n===== TOTALS =====")
    print(f"Total Employees: {totals['employees']}")
    print(f"Total Hours Worked: {totals['hours']}")
    print(f"Total Gross Pay: ${totals['gross']:.2f}")
    print(f"Total Income Tax: ${totals['tax']:.2f}")
    print(f"Total Net Pay: ${totals['net']:.2f}")

def main():
    employees = []  
    totals = {
        "employees": 0,
        "hours": 0.0,
        "gross": 0.0,
        "tax": 0.0,
        "net": 0.0
    }

    
    while True:
        name = get_employee_name()
        if name.lower() == "end":
            break

        from_date, to_date, hours_worked = get_dates_and_hours()
        hourly_rate = float(input("Enter hourly rate: "))
        tax_rate = float(input("Enter income tax rate (e.g., 0.20 for 20%): "))

        
        employee_record = [name, from_date, to_date, hours_worked, hourly_rate, tax_rate]
        employees.append(employee_record)

    
    process_employees(employees, totals)

    
    display_totals(totals)

if __name__ == "__main__":
    main()
