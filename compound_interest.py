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

if __name__ == "__main__":
    main()