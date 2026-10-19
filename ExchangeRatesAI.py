import os
import pandas as pd

#This is the code generated from vibe coding using Claude.

class ExchangeRates:
    """Reads Bank of Canada exchange rates from a CSV file using pandas
    and converts amounts between USD and CAD.
    """

    def __init__(self, filename):
        self.filename = filename
        self.rate_date = None
        self.usd_to_cad = None
        self._load_rates()

    def _load_rates(self):
        """Read the CSV with pandas and find the latest USD/CAD rate."""

        # Open the CSV file
        df = pd.read_csv(self.filename, encoding="utf-8-sig", parse_dates=["Date"])

        # Keep the date and USD/CAD columns, remove missing rates, sort by date
        rates = df[["Date", "FXAUSDCAD"]].dropna().sort_values("Date")

        # Save the most recent exchange rate
        latest = rates.iloc[-1]
        self.rate_date = latest["Date"].strftime("%Y-%m-%d")
        self.usd_to_cad = float(latest["FXAUSDCAD"])

    def convert(self, amount, from_currency, to_currency):
        """Convert an amount between USD and CAD."""

        # Convert USD to CAD
        if from_currency == "USD":
            return round(amount * self.usd_to_cad, 2)

        # Convert CAD to USD
        return round(amount / self.usd_to_cad, 2)


def main():

    # Find the CSV in the same folder as this Python file
    folder = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(folder, "BankOfCanadaExchangeRate.2026.csv")

    # Load the exchange rates
    rates = ExchangeRates(csv_path)

    # Welcome message
    print("=== USD / CAD Exchange Rate Calculator ===")
    print(f"Using Bank of Canada rate from {rates.rate_date}: "
          f"1 USD = {rates.usd_to_cad} CAD\n")

    # Allow the user to make multiple conversions
    while True:

        # Ask the user for the amount and currencies
        amount = float(input("Enter the amount to convert: "))
        from_currency = input("Convert FROM (USD or CAD): ")
        to_currency = input("Convert TO (USD or CAD): ")

        # Perform the conversion
        result = rates.convert(amount, from_currency, to_currency)

        # Display the result
        print(f"\n{amount:,.2f} {from_currency} = {result:,.2f} {to_currency}\n")

        # Ask if the user wants to convert again
        again = input("Convert another amount? (y/n): ")

        if again != "y":
            print("Goodbye!")
            break

        print()


# Start the program
if __name__ == "__main__":
    main()