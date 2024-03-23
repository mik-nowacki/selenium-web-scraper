from datetime import datetime

import pandas as pd


# search_results = pd.read_csv('search_results.csv')
#
# print(search_results['offer_date'][0])

search_time = datetime.now().strftime("%d/%m/%Y %H:%M")

print(search_time)