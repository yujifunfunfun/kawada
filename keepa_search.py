import keepa
import pandas as pd

api_key='abh5dml63es1k7q98c656ssfu3itlokh3oce9vdgfppf1j7172kmh7fh6d1tohfi'
api = keepa.Keepa(api_key)

products = api.query('4902370517033',product_code_is_asin=False,domain ='JP') # ここにはASINを入れるとデータを勝手に取ってくれます
print('Title is ' + products[0]['title'])