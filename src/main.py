from helper import load_stock_data
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
        print()
        choice = display_menu()
        if choice == '1':
            ticker = input("Enter the ticker of the stock you want to predict: ")
            df = load_stock_data(ticker)
            sma_last = lr_last = None
            sma_metrics = lr_metrics = None
            print(f"\nDataset for {ticker.upper()} loaded.\n")
        elif choice == '2':
            if df is None:
                print("\nPlease load the dataset first.\n")
                continue
            sma_last = sma_signal(df)
            sma_metrics = evaluate_sma(df)
            print("\n------ SMA (50-day) Results ------")
            if sma_last['signal'] == "Not enough data for SMA":
                print("Not enough data for SMA (need at least 50 rows).")
            else:
                print(f"Current Price: ${sma_last['current']:.2f}")
                print(f"SMA: ${sma_last['sma']:.2f}")
                print(f"Signal: {sma_last['signal']}")
            choice_v = input("\n[Press 'V' to view graph | Any key to continue...]\n")
            if choice_v.strip().lower() == 'v':
                compute_sma(df)
        elif choice == '3':
            if df is None:
                print("\nPlease load the dataset first.\n")
                continue
            lr_last = regression_signal(df)
            lr_metrics = evaluate_regression(df)
            print("\n------ Linear Regression Results ------")
            if lr_last['signal'] == "Not enough data for regression":
                print("Not enough data for regression (need at least 2 rows).")
            else:
                print(f"Predicted Next Day Price: ${lr_last['predicted']:.2f}")
                print(f"Signal: {lr_last['signal']}")
                print("\nRegression Coefficients:")
                print(f"- Slope (m): {lr_last['slope']:.2f}")
                print(f"- Intercept (b): {lr_last['intercept']:.2f}")
            choice_v = input("\n[Press 'V' to view graph | Any key to continue...]\n")
            if choice_v.strip().lower() == 'v':
                train_and_predict(df)
        elif choice == '4':
            if df is None:
                print("\nPlease load the dataset first.\n")
                continue
            # If not run yet, auto-evaluate
            if sma_metrics is None:
                sma_last = sma_signal(df)
                sma_metrics = evaluate_sma(df)
            if lr_metrics is None:
                lr_last = regression_signal(df)
                lr_metrics = evaluate_regression(df)
            print("\n------ Algorithm Comparison ------")
            print("| Metric        | SMA           | Linear Regression |")
            print("|---------------|---------------|-------------------|")
            print(f"| Accuracy      | {sma_metrics['accuracy']:.1f}%       | {lr_metrics['accuracy']:.1f}%             |")
            print(f"| Speed         | {sma_metrics['duration']:.2f} sec    | {lr_metrics['duration']:.2f} sec       |")
            print(f"| Simulated ROI | {sma_metrics['roi']:.1f}%       | {lr_metrics['roi']:.1f}%            |")
            print("\nConclusion: Linear Regression is more accurate but slower.\n")
        elif choice == '5':
            print("\nExiting program. Goodbye!\n")
            break
        else:
            print("\nInvalid choice. Please try again.\n")

if __name__ == "__main__":
    main()
