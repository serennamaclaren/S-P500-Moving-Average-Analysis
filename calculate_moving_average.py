import pandas as pd

def calculate_moving_averages(file_path, ticker='MMM', window_days='7D'):
    # 1. Load the dataset
    df = pd.read_csv(file_path)

    # 2. Pre-process the data
    # Convert pubDate to datetime objects
    df['pubDate'] = pd.to_datetime(df['pubDate'])

    # Filter for a specific company
    company_data = df[df['symbol'] == ticker].copy()

    # 3. Calculate Moving Average
    # Sort by date to ensure the rolling window is chronological
    company_data = company_data.sort_values('pubDate')

    # Set pubDate as index for time-based rolling window
    company_data.set_index('pubDate', inplace=True)

    # Calculate a rolling average of 'lm_score1' (sentiment score)
    # The '7D' window looks back 7 days from each point
    ma_column_name = f'sentiment_MA_{window_days}'
    company_data[ma_column_name] = company_data['lm_score1'].rolling(window=window_days).mean()

    return company_data

if __name__ == "__main__":
    # Path to the sentiment data file
    csv_file = '02_company_news_sentiment.csv'
    symbol = 'MMM'
    
    try:
        results = calculate_moving_averages(csv_file, ticker=symbol)
        
        print(f"--- Moving Average Sentiment for {symbol} (Last 10 entries) ---")
        print(results[['lm_score1', 'sentiment_MA_7D']].tail(10))
        
        # Save output to a new file
        output_name = f'{symbol}_sentiment_trends.csv'
        results.to_csv(output_name)
        print(f"\nResults saved to {output_name}")
        
    except FileNotFoundError:
        print(f"Error: {csv_file} not found. Please ensure the file is in the same directory.")
