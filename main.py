import eel
from amazon import *
from kawada import *
from cal_profit import *

def keyword_modify(keyword_str):
    keyword_list = keyword_str.splitlines()
    return keyword_list


@eel.expose
def main(keyword_str):
    keyword_list = keyword_modify(keyword_str)
    kawada_item_data = fetch_kawada_data(keyword_list)
    amazon_item_data = fetch_amazon_data(kawada_item_data) 
    cal_profit(kawada_item_data,amazon_item_data)  

eel.init("web")
eel.start("main.html")