# Import necessary libraries
import pandas as pd
import spacy

# Download the spacy model
nlp = spacy.load("en_core_web_sm")

# Helper functions for text preprocessing (data cleaning) section
def lower_replace(series):
    output = series.str.lower()
    output = output.str.replace(r'\[.*?\]', '', regex=True)
    output = output.str.replace(r'[^\w\s]', '', regex=True)
    return output

def token_lemma_nonstop(text):
    doc = nlp(text)
    output = [token.lemma_ for token in doc if not token.is_stop]
    return ' '.join(output)

def clean_and_normalize(series):
    output = lower_replace(series)
    output = output.apply(token_lemma_nonstop)
    return output

# Helper function for EDA in the recommender section
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

# Allow command-line execution
if __name__ == "__main__":
    print("Text preprocessing module ready to use.")