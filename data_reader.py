import pandas as pd

googler_output = pd.read_csv('googler_output.csv', sep=';')
output_scraper = pd.read_csv('output_scrapper.csv', sep=';')

print(googler_output.head())
print(googler_output.columns)
print('############################################################')
print(output_scraper.head())
print(output_scraper.columns)

