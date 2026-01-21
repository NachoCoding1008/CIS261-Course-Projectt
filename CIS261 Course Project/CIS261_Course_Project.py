#Elijah Figaro
#CIS 261
#CIS 261 Course Project

def get_employee_name():
    return input("Enter employee name (or End to quit): ")

def get_total_hours():
    return float(input("Enter total hours worked: "))

def get_hourly_rate():
    return float(input("Enter hourly rate: "))

def get_tax_rate():
    return float(input("Enter income tax rate (e.g., .15 for 15%): "))

def calculate_pay(hours, rate, tax_rate):
    gross_pay = hours * rate
    income_tax = gross_pay * tax_rate
    net_pay = gross_pay - income_tax
    return gross_pay, income_tax, net_pay

def display_employee(name, hours, rate, gross, tax_rate, tax, net):
    print("\nEmployee Summary")
    print(f"Name: {name}")
    print(f"Hours Worked: {hours}")
    print(f"Hourly Rate: ${rate:.2f}")
    print(f"Gross Pay: ${gross:.2f}")
    print(f"Tax Rate: {tax_rate:.2%}")
    print(f"Income Tax: ${tax:.2f}")
    print(f"Net Pay: ${net:.2f}")
    
def display_totals(emp_count, total_hours, total_gross, total_tax, total_net):
    print("\nPayroll Totals")
    print(f"Total Employees: {emp_count}")
    print(f"Total Hours: {total_hours}") 
    print(f"Total Gross Pay: ${total_gross:.2f}")
    print(f"Total Tax: ${total_tax:.2f}") 
    print(f"Total Net Pay: ${total_net:.2f}")

employee_count = 0
total_hours = total_gross = total_tax = total_net = 0

while True:
    employee_name = get_employee_name()
    if employee_name == "End":
        break

    hours = get_total_hours()
    rate = get_hourly_rate()
    tax_rate = get_tax_rate()

    gross, tax, net = calculate_pay (hours, rate, tax_rate)

    display_employee(employee_name, hours, rate, gross, tax_rate, tax, net)

    employee_count += 1
    total_hours += hours
    total_gross += gross
    total_tax += tax
    total_net += net

display_totals(employee_count, total_hours, total_gross, total_tax, total_net)


