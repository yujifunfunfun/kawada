import os
from dotenv import load_dotenv
from logger import set_logger
load_dotenv() #環境変数のロード
from logger import set_logger
logger = set_logger(__name__)
from sp_api.api import Catalog
from sp_api.api import ProductFees
from sp_api.api import Products

from sp_api.base.marketplaces import Marketplaces


def fetch_amazon_data(kawada_item_data):
    amazon_item_data = []
    for kawada_item in kawada_item_data:
        jan = kawada_item[0]
        print(jan)
        hits_item =  Catalog(Marketplaces.JP).list_items(JAN=jan).payload.get('Items')
        if len(hits_item) == 0:
            price = 0
            buybox_price = 0
            item_url = 'None'
        elif len(hits_item) == 1:
            try:
                asin = hits_item[0].get('Identifiers').get('MarketplaceASIN').get('ASIN')
                item_data = Products(Marketplaces.JP).get_item_offers(asin=asin,ItemCondition='New')
                buybox_price = item_data.payload.get('Summary').get('BuyBoxPrices')[0].get('ListingPrice').get('Amount') 
                item_url = f'https://www.amazon.co.jp/gp/product/{asin}'
                fba_fee = cal_fba_fee(asin,buybox_price)
                price = buybox_price - fba_fee
            except Exception as e:
                price = 0
                buybox_price = 0
                item_url = 'None'
                logger.info(e)
            amazon_item_data.append([price,buybox_price,item_url])
        else:
            buybox_price_list = []
            price_list = []
            item_url_list = []
            for n in range(len(hits_item)):
                try:
                    asin = hits_item[n].get('Identifiers').get('MarketplaceASIN').get('ASIN')
                    item_data = Products(Marketplaces.JP).get_item_offers(asin=asin,ItemCondition='New')
                    buybox_price = item_data.payload.get('Summary').get('BuyBoxPrices')[0].get('ListingPrice').get('Amount') 
                    item_url = f'https://www.amazon.co.jp/gp/product/{asin}'
                    fba_fee = cal_fba_fee(asin,buybox_price)
                    price = buybox_price - fba_fee
                    buybox_price_list.append(buybox_price)
                    price_list.append(price)
                    item_url_list.append(item_url)
                except Exception as e:
                    logger.info(e)
            amazon_item_data.append([price_list,buybox_price_list,item_url_list])
    print(amazon_item_data)
    return amazon_item_data


def cal_fba_fee(asin,price):
    try:
        fees_data = ProductFees(Marketplaces.JP).get_product_fees_estimate_for_asin(asin=asin,price=price,currency='JPY',is_fba=True)
        fba_fee = fees_data.payload.get('FeesEstimateResult').get('FeesEstimate').get('TotalFeesEstimate').get('Amount')
    except Exception as e:
        fba_fee = 999999
    return fba_fee


if __name__ == "__main__":
    fetch_amazon_data()