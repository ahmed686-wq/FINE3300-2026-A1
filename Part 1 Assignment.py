
import csv

# Assignment Part 1 

# The Class for exchange rates
class ExchangeRates:

    def __init__(self, file):
        self._file = file

        # This is to open the CSV file and extract the exchange rate
        with open(self._file, "r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
         # This is to loop through the rows in the CSV file and find the latest exchange rate
            for row in reader:
                if row["FXAUSDCAD"]:
                    self._rate = float(row["FXAUSDCAD"])


    # Function to convert between USD and CAD
    def convert(self, amount, current_currency, to_currency):

        if current_currency == "USD" and to_currency == "CAD":
            return amount * self._rate

        elif current_currency == "CAD" and to_currency == "USD":
            return amount / self._rate

# Create the currency converter using the CSV file
converter = ExchangeRates("BankOfCanadaExchangeRate.2026.csv")


# Keep running the program until the user wants to stop doing the conversions
while True:

    # Question 1: Ask which currency to convert
    currency = input("Do you want to convert USD to CAD or CAD to USD? Type 'USD to CAD' or 'CAD to USD': ")

    # Question 2: Ask for the amount
    amount = float(input("Enter the amount you want to convert: "))

    # Check which currency the user selected and perform the conversion
    if currency == "USD to CAD":
    
        result = converter.convert(amount, "USD", "CAD")
        print("${:.2f} USD = ${:.2f} CAD".format(amount, result))

    elif currency == "CAD to USD":

        result = converter.convert(amount, "CAD", "USD")
        print("${:.2f} CAD = ${:.2f} USD".format(amount, result))
    
    # This is to check if the currency selection is valid. If it is not, it prints an error message and continues the loop to ask for the currency again.
    else:
        print("Invalid currency selection")

    # Ask if the user wants to convert again
    restart = input("Do you want to convert again? (type: yes/no): ")

    # this the user input to check if they want to continue or not. the lower function is used to make the input insensitive to Uppercase and lowercase letters. If the user types anything other than "yes", the program will print "finish" and break out of the loop, ending the program.
    if restart.lower() != "yes":
        print("finish")
        break
