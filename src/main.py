from utils import load_stock_data
from sma import compute_sma, sma_signal, evaluate_sma
from linear_regression import train_and_predict, regression_signal, evaluate_regression

def display_menu():
    print("=== Stock Trend Predictor by Josh Caron and Nico Lara ===")
    print("1. Load Dataset")
    print("2. Run SMA Prediction")
    print("3. Run Linear Regression Prediction")
    print("4. Compare Results")
    print("5. Exit")
    return input("\n> Select option: ")

def main():
    df = None
    sma_last = None
    lr_last = None
    sma_metrics = None
    lr_metrics = None

    while True:
        choice = display_menu()

        if choice == '1':
            ticker = input("Enter the ticker of the stock you want to predict: ")
            df = load_stock_data(ticker)
            print(f"\nDataset for {ticker.upper()} loaded.\n")

        elif choice == '2':
            if df is None:
                print("\nPlease load the dataset first.\n")
                continue
            sma_last = sma_signal(df)
            sma_metrics = evaluate_sma(df)
            print("\n------ SMA (50-day) Results ------")
            print(f"Current Price: ${sma_last['current']:.2f}")
            print(f"SMA: ${sma_last['sma']:.2f}")
            print(f"Signal: {sma_last['signal']}")
            input("\n[Press 'V' to view graph | Any key to continue...]")
            compute_sma(df)

        elif choice == '3':
            if df is None:
                print("\nPlease load the dataset first.\n")
                continue
            lr_last = regression_signal(df)
            lr_metrics = evaluate_regression(df)
            print("\n------ Linear Regression Results ------")
            print(f"Predicted Next Day Price: ${lr_last['predicted']:.2f}")
            print(f"Signal: {lr_last['signal']}")
            print("\nRegression Coefficients:")
            print(f"- Slope (m): {lr_last['slope']:.2f}")
            print(f"- Intercept (b): {lr_last['intercept']:.2f}")
            input("\n[Press 'V' to view graph | Any key to continue...]")
            train_and_predict(df)

        elif choice == '4':
            if sma_metrics is None or lr_metrics is None:
                print("\nPlease run both SMA and Regression predictions first.\n")
                continue
            print("\n------ Algorithm Comparison ------")
            print("| Metric        | SMA           | Linear Regression |")
            print("|---------------|---------------|-------------------|")
            print(f"| Accuracy      | {sma_metrics['accuracy']:.1f}%       | {lr_metrics['accuracy']:.1f}%             |")
            print(f"| Speed         | {sma_metrics['duration']:.2f} sec    | {lr_metrics['duration']:.2f} sec       |")
            print(f"| Simulated ROI | {sma_metrics['roi']:.1f}%       | {lr_metrics['roi']:.1f}%            |")
            print("\nConclusion: Linear Regression is more accurate but slower.\n")

        elif choice == '5':
            print("\nExiting program. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please try again.\n")

if __name__ == "__main__":
    main()
