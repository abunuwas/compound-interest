import sys
import csv
import re

def getData(file):
    "Uses processFile function to process the data from a csv file and return a list of tuples"
    
    rates = []
    with open(file) as file:
        rates = processFile(file, rates)
    return rates

def processFile(file, rates):
    """
    Returns a list in which every member is a tuple, where the first member
    is the interest rate and the second member amount lent at that rate. The
    function expects a csv file where two headers are 'Rate' and 'Available'.
    The values in the columns of those headers must be digits.
    Parameters:
    ----------
    file: a csv file already opened with open().
    rates: a list. 
    """
    
    data = csv.DictReader(file)
    for row in data:
        try:
            rates.append((float(row['Rate']), float(row['Available'])))
        except ValueError:
            print('It seems that the file contains corrupted data. Please ensure that \
all the values in the Rate column and the Available column are digits')
            raise SystemExit
    return rates

def sortData(data):
    "Order the amounts available for lending according to their interest rate, from lowest to highest"
    
    return sorted(data, key=lambda values: values[0])

def buildLend(quantity_borrow, lending_data):
    """
    Returns a list of tuples, where the first member in the tuple is the interest rate, and the second
    the amount available for lending, up to the borrowing amount requested by the borrower.
    parameters:
    ----------
    quantity_borrow: amount that the borrower wishes to borrow.
    lending_data: a list where every member of the list must be an iterable. The first member of this element
                  must represent interest rates, and the second element the amount available for lending
                  at that interest rate. 
    """
    
    apply_ceiling = lambda amount, quantity, ceiling: quantity if amount+quantity<=1000 else ceiling-amount
    amount = 0
    needed_rates = []
    for rate, quantity in lending_data:
        if amount < 1000:
            quantity = apply_ceiling(amount, quantity, quantity_borrow)
            amount += quantity       
            needed_rates.append((rate, quantity))
    return needed_rates

def compoundInterest(principal, annual_rate, years, compounding_base):
    """
    Simple implementation of common formula for the calculation of an amount after applying compounding
    interest rates.
    Parameters:
    ----------
    principal: the amount that will be borrowed.
    annual_rate: the annual rate of return.
    years: the number of years over which the loan will be held.
    compounding_base: the rate of compounding. 
    """
    
    outcome = principal * ((1 + (annual_rate / compounding_base))**(years * compounding_base))
    return outcome

def calculateFinalPayment(lending_data, time, compounding_rate):
    """
    Returns the total amount that the borrower will pay after applying the compound interest rate.
    Parameters:
    ----------
    lending_data: a list, where every member is an iterable; first member of the iterable must be the interest
                  rate, and the second the amount of money available at that interest rate.
    time: the number of years over which the loan will be held.
    compounding_rate: the rate of compounding. 
    """
    
    outcome = []
    for rate, quantity in lending_data:
        final_quantity = compoundInterest(quantity, rate, time, compounding_rate)
        outcome.append(final_quantity)
    return sum(outcome)

def calculateAverageWeightedRate(lending_data):
    """
    Given information about different amounts of money which will be borrowed at different interest rates,
    this function returns the average interest rate, weighted by the amount of money that will be borrowed
    at each rate.
    Parameters:
    ----------
    lending_data: a list, where every member is an iterable; first member of the iterable must be the interest
                  rate, and the second the amount of money available at that interest rate.
    """
    
    amount_borrowed = sum([quantity for rate, quantity in lending_data])
    weighted_rates = []
    for rate, quantity in lending_data:
        weight = quantity / amount_borrowed
        weighted_rate = rate * weight
        weighted_rates.append(weighted_rate)
    return sum(weighted_rates)

def getMonthlyPayments(final_payment, months):
    "Returns the monthly installments of a total payment, given the number of months. "
    return final_payment / months

def monthToYears(num_months):
    return num_months / 12

def getFile():
    """
    Checks that the first argument provided in the command-line for this application is a file in .csv format.
    If the data is not valid, the application displays an error message and exits. 
    """
    
    file_error = 'Please provide a valid file value.'
    try:
        file = sys.argv[1]
    except IndexError:
        print(file_error)
        raise SystemExit
    if file.endswith('.csv'):
        return file
    else:
        print(file_error)
        raise SystemExit

def getPrincipal():
    """
    Checks that the second argument provided in the command-line for this application is a positive number,
    disivible by 100 and no bigger than 15000. If the data is not valid, the application displays an error
    message and exits. 
    """
    
    principal_error = 'Please provide a valid value for your borrowing quantity.'
    try:
        principal = sys.argv[2]
    except IndexError:
        print(principal_error)
        raise SystemExit
    if re.match('\d+[.,]?(\d+)?', principal):
        if (float(principal) > 0
            and float(principal) % 100 == 0
            and float(principal) <= 15000):
            return float(principal)
        else:
            print(principal_error)
            sys.exit()
    else:
        print(principal_error)
        sys.exit()
        
def getMonths():
    """
    Checks that the third argument provided in the command-line for this application is a positive integer
    number. If the data is not valid, the application displays an error message and exits. 
    """
    
    try:
        months = sys.argv[3]
    except IndexError:
       print('You have not choosen a borrowing period. We asume you want \
to borrow your money for 12 months.')
       return 12
    if re.match('\d+', months):
        if (float(months) > 0 and float(months).is_integer()):
            return float(months)
        else:
            print('Please provide a valid number of months.')
            sys.exit()
    else:
        print('Please provide a valid number of months.')
        sys.exit()
        
def produceFinalValues(file, principal, months):
    years = monthToYears(months)
    lending_data = getData(file)
    lending_data = sorted(lending_data)
    needed_rates = buildLend(principal, lending_data)
    total_payment = calculateFinalPayment(needed_rates, years, 12)
    weighted_average_rate = calculateAverageWeightedRate(needed_rates)
    monthly_payments = getMonthlyPayments(total_payment, months)
    return round(weighted_average_rate*100, 1), round(monthly_payments, 2), round(total_payment, 2)

def displayInformation(principal, rate, monthly, total):
    message = '''
Requested amount: £{amount:.0f}
Rate : {rate}%
Monthly repayment: £{monthly}
Total repayment: £{total}
'''.format(amount=principal, rate=rate, monthly=monthly, total=total)
    return message

welcome_message = '''
Welcome to the best application for borrowers in the Universe!
Here you'll find the lowest rates in the market for any loan you
want to take. Please notice that we can't provide loans for amounts
bigger than £15.000. On the other hand, who needs so much money??
You can request any amount from £100 to £15.000 in increases of 
£100. This is by design. We've figured out that life has more meaning
when loans are borrowed in multiples of 100. We apply an interest
rate compounded on a monthly basis. This is to your advantage, it
means we don't increase the rate every second or less! You can select
for how long you want to borrow the loan, by specifying the number of
months in the third argument to the command-line input after invoking
the file. If you don't, we assume you want to take the loan for one
year (solar year, if you were wondering). 
'''

def main():
    print(welcome_message)
    import sys
    file = getFile()
    principal = getPrincipal()
    months = getMonths()
    rate, monthly, total = produceFinalValues(file, principal, months)
    information = displayInformation(principal, rate, monthly, total)
    print(information)

if __name__ == "__main__":
    main()
