def get_percentiles(df, column):
    """
    Prints out seven percentiles of an input column from the input DataFrame. Specifically, the 1st, 5th, 
    25th, 50th, 75th, 95th, and 99th percentiles.
    
    Inputs:
        - df (pd.DataFrame)
        - column (str)
    Returns:
        - None
    """
    percentiles = [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]
    for percentile in percentiles:
        print(f'{column} - {percentile} percentile: {df[column].quantile(percentile)}')

# allow command-line execution
if __name__ == "__main__":
    print("Text preprocessing module ready to use.")