import pandas as pd

search_results = pd.read_csv('search_results.csv')

print(search_results['offer_date'][0])