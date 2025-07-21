# Import necessary libraries
import pandas as pd
import spacy
from tqdm import tqdm

# Adds progress bar to pd.DataFrame.apply method
tqdm.pandas()

# Download the spacy model
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

# Helper functions for text preprocessing (data cleaning) section
def lower_replace(series):
    output = series.str.lower()                                # Turn all uppercase characters to lowercase
    output = output.str.replace(r'[^\w\s]', '', regex=True)    # Remove all punctution
    output = output.str.replace(r'\s*\n', '', regex=True)      # Remove '\n' and leading whitespace
    return output

def clean_and_normalise(series):
    cleaned = lower_replace(series).fillna('')                 # lowercase, remove punctuation, and remove NaN values
    processed_texts = nlp.pipe(cleaned, batch_size=1000)       # process texts in batches with nlp.pipe()
    
    # lemma and remove stopwords for each doc
    output = []
    for doc in tqdm(processed_texts, total=len(series)):
        tokens = [token.lemma_ for token in doc if not token.is_stop]
        output.append(' '.join(tokens))
    
    return pd.Series(output)

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
    print("functions module ready to use.")