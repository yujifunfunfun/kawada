import pandas as pd


def cal_profit(kawada_item_data,amazon_item_data):
    cols = ['利益','利益率','商品名','カワダ価格','Amazonカート価格-FBA手数料','Amazonカート価格','カワダURL','amazonURL']
    profit_df = pd.DataFrame(index=[], columns=cols)
    for kawada_item,amazon_item in zip(kawada_item_data,amazon_item_data):
        item_name = kawada_item[1]
        kawada_price = kawada_item[2]
        kawada_url = kawada_item[3]
        amazon_price = amazon_item[0]
        print(amazon_price)
        amazon_buybox_price = amazon_item[1]
        amazon_url = amazon_item[2]

        if type(amazon_price) == list:
            price_data_num = len(amazon_price)
            profit_list = []
            profit_rate_list = []
            for n in range(price_data_num):
                print(amazon_price[n])
                profit = int(kawada_price) - int(amazon_price[n])
                profit_rate = profit / amazon_price[n] * 100
                profit_list.append(profit)
                profit_rate_list.append(profit_rate)

            record = pd.Series([profit_list,profit_rate_list,item_name,kawada_price,amazon_price,amazon_buybox_price,kawada_url,amazon_url], index=profit_df.columns)
            profit_df = profit_df.append(record, ignore_index=True)
        else:
            profit = int(kawada_price) - int(amazon_price)
            profit_rate = profit / amazon_price * 100
            record = pd.Series([profit,profit_rate,item_name,kawada_price,amazon_price,amazon_buybox_price,profit,profit_rate,kawada_url,amazon_url], index=profit_df.columns)
            profit_df = profit_df.append(record, ignore_index=True)
    profit_df.to_csv("profit.csv",encoding="utf_8-sig",header=False,index=False)
    


