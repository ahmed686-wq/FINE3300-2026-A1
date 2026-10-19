
import os
import pandas as pd


class ExchangeRates:
    """Reads Bank of Canada exchange rates from a CSV file using pandas
    and converts amounts between USD and CAD.
    """

    RATE_COLUMN = "FXAUSDCAD"
    SUPPORTED = ("USD", "CAD")

    def __init__(self, filename):
        self.filename = filename
        self.rate_date = None
        self.usd_to_cad = None
        self._load_rates()

    def _load_rates(self):
        """Read the CSV with pandas and find the latest USD/CAD rate."""

        # Open the CSV file
        df = pd.read_csv(
            self.filename,
            encoding="utf-8-sig",
            parse_dates=["Date"]
        )

        # Check that the exchange rate column exists
        if self.RATE_COLUMN not in df.columns:
            raise ValueError(
                f"Column '{self.RATE_COLUMN}' was not found in {self.filename}"
            )

        # Remove missing rates and sort by date
        rates = (
            df[["Date", self.RATE_COLUMN]]
            .dropna(subset=["Date", self.RATE_COLUMN])
            .sort_values("Date")
        )

        # Check if there are any exchange rates
        if rates.empty:
            raise ValueError(f"No USD/CAD rate found in {self.filename}")

        # Save the most recent exchange rate
        latest = rates.iloc[-1]

        self.rate_date = latest["Date"].strftime("%Y-%m-%d")
        self.usd_to_cad = float(latest[self.RATE_COLUMN])

    def convert(self, amount, from_currency, to_currency):
        """Convert an amount between USD and CAD."""

        from_currency = from_currency.strip().upper()
        to_currency = to_currency.strip().upper()

        # Check supported currencies
        for currency in (from_currency, to_currency):
            if currency not in self.SUPPORTED:
                raise ValueError(
                    f"Unsupported currency '{currency}'. Use USD or CAD."
                )

        # If both currencies are the same
        if from_currency == to_currency:
            return round(float(amount), 2)

        # Convert USD to CAD
        if from_currency == "USD":
            return round(amount * self.usd_to_cad, 2)

        # Convert CAD to USD
        return round(amount / self.usd_to_cad, 2)


def ask_amount():
    """Ask the user for a valid amount."""

    while True:
        text = input("Enter the amount to convert: ").strip().replace(",", "")

        try:
            amount = float(text)

            if not 0 <= amount < float("inf"):
                print("Please enter a non-negative, finite amount.")
                continue

            return amount

        except ValueError:
            print("That's not a valid number. Try again.")


def ask_currency(prompt):
    """Ask the user to enter USD or CAD."""

    while True:
        currency = input(prompt).strip().upper()

        if currency in ExchangeRates.SUPPORTED:
            return currency

        print("Please enter either USD or CAD.")


def main():

    # Find the CSV in the same folder as this Python file
    folder = os.path.dirname(os.path.abspath(__file__))

    # Correct CSV filename
    csv_path = os.path.join(
        folder,
        "BankOfCanadaExchangeRate.2026.csv"
    )

    # Load the exchange rates
    try:
        rates = ExchangeRates(csv_path)

    except FileNotFoundError:
        print(f"Could not find the exchange rate file:\n{csv_path}")
        print("Make sure the CSV is in the same folder as this script.")
        return

    except ValueError as err:
        print(f"Problem reading the exchange rate file: {err}")
        return

    # Welcome message
    print("=== USD / CAD Exchange Rate Calculator ===")

    print(
        f"Using Bank of Canada rate from {rates.rate_date}: "
        f"1 USD = {rates.usd_to_cad} CAD\n"
    )

    # Allow the user to make multiple conversions
    while True:

        # Ask the user for an amount
        amount = ask_amount()

        # Ask which currencies to convert
        from_currency = ask_currency("Convert FROM (USD or CAD): ")
        to_currency = ask_currency("Convert TO (USD or CAD): ")

        # Perform the conversion
        result = rates.convert(amount, from_currency, to_currency)

        # Display the result
        print(
            f"\n{amount:,.2f} {from_currency} = "
            f"{result:,.2f} {to_currency}\n"
        )

        # Ask if the user wants to convert again
        again = input("Convert another amount? (y/n): ").strip().lower()

        if again != "y":
            print("Goodbye!")
            break

        print()


# Start the program
if __name__ == "__main__":
    main()
