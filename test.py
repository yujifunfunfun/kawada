import os
from dotenv import load_dotenv
from logger import set_logger
load_dotenv() #環境変数のロード
from logger import set_logger
logger = set_logger(__name__)
from sp_api.api import Catalog
from sp_api.api import CatalogItems

from sp_api.api import ProductFees
from sp_api.api import Products

from sp_api.base.marketplaces import Marketplaces



# asin = Catalog(Marketplaces.JP).list_items(JAN=4970381192754)
# item_data = Products(Marketplaces.JP).get_item_offers(asin='B08M1749BX',ItemCondition='New')


amazon_item_data = [[[100,200],200,300],[100,200,300]]
amazon_item = [[100,200],200,300]
amazon_item[0] = [100,200]
print(asin)


4970381192754,4970381188894,4970381502843,4970381500146,4902370533644,4902370533651,4902370533668,4905040307309,0630509733446,4970381175924,4548565366583,4548565366590,4548565383764,4548565383771,4548565383788,4548565387823,4902370517033,4902370517026,4902370516517,4902370516524,4902370516531,4902370516548,4902370516555,4902370516562,4902370519686,4902370621013,4902370502749,4902370519280,4902370516838,4902370516821,4902370516845,4902370518306,4902370518313,4902370518320

4902370516845

4905040307309
4902370533651