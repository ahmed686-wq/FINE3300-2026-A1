
import csv

# Assignment Part 1 

# Class for exchange rate conversions
class ExchangeRates:

    def __init__(self, file):
        self._file = file

        # Open the CSV file and extract the exchange rate
        with open(self._file, "r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                if row["FXAUSDCAD"]:
                    self._rate = float(row["FXAUSDCAD"])


    # Function to convert between USD and CAD
    def convert(self, amount, current_currency, to_currency):

        if current_currency == "USD" and to_currency == "CAD":
            return amount * self._rate

        elif current_currency == "CAD" and to_currency == "USD":
            return amount / self._rate

        else:
            return amount


# Create the currency converter using the CSV file
converter = ExchangeRates("BankOfCanadaExchangeRate.2026.csv")


# Keep running the program until the user wants to stop
while True:

    # Question 1: Ask which currency to convert
    currency = input("Do you want to convert USD to CAD or CAD to USD? ")

    # Question 2: Ask for the amount
    amount = float(input("Enter the amount you want to convert: "))

    # Check which currency the user selected
    if currency == "USD to CAD":

        result = converter.convert(amount, "USD", "CAD")
        print(f"${amount:.2f} USD = ${result:.2f} CAD")

    elif currency == "CAD to USD":

        result = converter.convert(amount, "CAD", "USD")
        print(f"${amount:.2f} CAD = ${result:.2f} USD")

    else:
        print("Invalid currency selection")

    # Ask if the user wants to convert again
    restart = input("Do you want to convert again? (yes/no): ")

    if restart.lower() != "yes":
        print("finish")
        break
