import sys
import csv
import re

def getData(file):
    rates = []
    with open(file) as file:
        rates = processFile(file, rates)
    return rates

def processFile(file, rates):
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
    return sorted(data, key=lambda values: values[0])

def buildLend(quantity_borrow, lending_data):
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
    outcome = principal * ((1 + (annual_rate / compounding_base))**(years * compounding_base))
    return outcome

def calculateFinalPayment(lending_data, time, compounding_rate):
    outcome = []
    for rate, quantity in lending_data:
        final_quantity = compoundInterest(quantity, rate, time, compounding_rate)
        outcome.append(final_quantity)
    return sum(outcome)

def calculateAverageWeightedRate(lending_data):
    amount_borrowed = sum([quantity for rate, quantity in lending_data])
    weighted_rates = []
    for rate, quantity in lending_data:
        weight = quantity / amount_borrowed
        weighted_rate = rate * weight
        weighted_rates.append(weighted_rate)
    return sum(weighted_rates)

def getMonthlyPayments(final_payment, months):
    return final_payment / months

def monthToYears(num_months):
    return num_months / 12

def produceFinalValues(file, principal, months):
    years = monthToYears(months)
    lending_data = getData(file)
    lending_data = sorted(lending_data)
    needed_rates = buildLend(principal, lending_data)
    total_payment = calculateFinalPayment(needed_rates, years, 12)
    weighted_average_rate = calculateAverageWeightedRate(needed_rates)
    monthly_payments = getMonthlyPayments(total_payment, months)
    return weighted_average_rate, monthly_payments, total_payment

def getFile():
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
        

def main():
    import sys
    file = getFile()
    principal = getPrincipal()
    months = getMonths()
    print(file, principal, months)

    data = getData('market.csv')
    for row in data:
    	print(row)

if __name__ == "__main__":
    main()