import math
import argparse

parser = argparse.ArgumentParser(description="")
parser.add_argument('--type', type=str, default=None, help="Required. Enter annuity(=precise payments) or diff(=loan principal is reduced by a constant amount each month)")
parser.add_argument('--payment', type=float, default=None, help="One payment amount")
parser.add_argument('--principal',type=float, default=None, help="The amount of the loan")
parser.add_argument('--periods', type=int, default=None, help="How many months")
parser.add_argument('--interest', type=float, default=None, help="Bank interest payment")

args = parser.parse_args()

if args.type not in ("annuity", "diff") or args.type is None:
    print("Incorrect parameters")
    exit()
if args.type == "diff" and args.payment is not None:
    print("Incorrect parameters")
    exit()
if args.interest is None:
    print("Incorrect parameters")
    exit()   
for arg in (args.payment, args.principal, args.periods, args.interest):
    if arg is not None:
        if int(arg) < 0:
            print("Incorrect parameters")

undefined = [arg for arg in vars(args) if getattr(args, arg) is None]

if len(undefined) > 1:
    print("Incorrect parameters")
    exit()

# Calculate for annuity payments
def payment_calculus():
    """Get monthly payment amount"""
    rate = args.interest / (12 * 100)
    monthly = ((rate * math.pow(1 + rate, args.periods)/(math.pow(1 + rate, args.periods) - 1))) * args.principal
    return monthly

def loan_calculus():
    """Get overall loan amount"""
    rate = args.interest / (12 * 100)
    loan = args.payment / ((rate * math.pow(1 + rate, args.periods)/(math.pow(1 + rate, args.periods) - 1)))
    return loan

def months_calculus():
    """Count how many periods it will take to cover the loan"""
    rate = args.interest / (12 * 100)
    periods = math.log(args.payment / (args.payment - (rate * args.principal)), 1 + rate)
    return periods

def years_months(periods):
    """Converse periods in years and months"""
    month = int(periods) if (periods - int(periods)) == 0.0 else int(periods+1)
    years, months = divmod(month, 12)
    letter_month = '' if months == 1 else 's'
    letter_year = '' if years == 1 else 's'
    if months > 0 and years > 0:
        print(f"It will take {years} year{letter_year} and {months} month{letter_month} to repay this loan!")
    elif months > 0 and years == 0:
        print(f"It will take {months} month{letter_month} to repay this loan!")
    else:
        print(f"It will take {years} year{letter_year} to repay this loan!")
    return month

def overpayment(payment: float, periods: int, loan: int):
    """"""
    overpayment__amount = int(payment * periods - loan)
    print(f'\nOverpayment = {overpayment__amount}')

def differential():
    """Calculate differential payments"""
    rate = args.interest / (12 * 100)
    sum_diff = 0
    for i in range(1, args.periods+1):
        diff = (args.principal / args.periods) + rate * (args.principal - (args.principal * (i - 1) / args.periods))
        payment = int(diff) if diff - int(diff) == 0.0 else int(diff+1)
        print(f"Month {i}: payment is {payment}")
        sum_diff += payment
    overpayment = int(sum_diff - args.principal)
    print(f"\nOverpayment = {overpayment}")

if args.type == 'annuity':
    if undefined[0] == 'payment':
        payment = int(payment_calculus() + 1)
        print(f"Your monthly payment = {payment}!")
        overpayment(payment, args.periods, args.principal)
    elif undefined[0] == 'principal':
        amount = int(loan_calculus())
        print(f"Your loan principal = {amount}!")
        overpayment(args.payment, args.periods, amount)
    elif undefined[0] == 'periods':
        periods = months_calculus()
        months = years_months(periods)
        overpayment(args.payment, months, args.principal)
elif args.type == 'diff':
    differential()
