import os
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

# Initialize the sentiment intensity analyzer
sid = SentimentIntensityAnalyzer()

# sentiment analysis
def analyze_sentiment(text):
    text = str(text)
    analysis = sid.polarity_scores(text)
    return analysis['compound']

directory = 'C:/Users/jucas/Desktop/MD-Projeto/2014'

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.xlsx'):
        df = pd.read_excel(os.path.join(directory, filename), engine='openpyxl')
        
        df['Sentiment'] = df['Review'].apply(analyze_sentiment)
        
        sentiment_average = df['Sentiment'].mean()
        rating_average = df['Rating'].mean()

        # Normalize sentiment
        sentiment_average = (sentiment_average + 1) * 5 

        # Round the averages to one decimal
        sentiment_average = round(sentiment_average, 1)
        rating_average = round(rating_average, 1)

        sentiment_average = f'{sentiment_average}/10'
        rating_average = f'{rating_average}/10'

        # Create a new DataFrame with the averages
        averages_df = pd.DataFrame({'Sentiment': [sentiment_average], 'Rating': [rating_average]}, index=['Average'])
        
        # Append averages to the bottom of the original DataFrame
        df_with_averages = df.append(averages_df, ignore_index=False)

        # Create a new filename for the output
        new_filename = f'{os.path.splitext(filename)[0]}_sentiment.xlsx'
        
        # Save the results without including the DataFrame's index
        df_with_averages.to_excel(os.path.join(directory, new_filename), index=False)
