import os
import pandas as pd

directory = 'C:/Users/jucas/Desktop/MD-Projeto/2014'


data = {'Filename': [], 'Sentiment_Average': [], 'Rating_Average': []}

for filename in os.listdir(directory):
    if filename.endswith('_sentiment.xlsx'):
        df = pd.read_excel(os.path.join(directory, filename), engine='openpyxl')
        
        # Get the averages row
        averages_row = df.iloc[-1]  # Get the last row
        
        data['Filename'].append(filename)
        data['Sentiment_Average'].append(averages_row['Sentiment'])
        data['Rating_Average'].append(averages_row['Rating'])

summary_df = pd.DataFrame(data)

summary_df = summary_df.sort_values(by='Sentiment_Average', ascending=False)

summary_df.to_excel(os.path.join(directory, 'summary_sentiment.xlsx'), index=False)