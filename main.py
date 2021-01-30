import time
from threading import Thread
from random import seed
from random import randint
import math
seed(2)
medianBuy = 33900
medianSell = 34100
# priceMinBuy = float(30000)
# priceMaxBuy = float(32500)
# priceMinSell = float(35000)
# priceMaxSell = float(40000)

from kucoin.client import Market
#client = Market(url='https://api.kucoin.com')
#client = Market()

# or connect to Sandbox
market = Market(url='https://openapi-sandbox.kucoin.com')
market = Market(is_sandbox=True)
api_key = '5fba3c542bf81d000732c33a'
api_secret = '9ea92efa-107d-4b7a-b5fd-e10e5e179f39'
api_passphrase = 'uosisfuturo'
def returnBid(symbol):
    book = market.get_aggregated_order(symbol)
    return book['bids'][1][0]
# print(bid)
# book = client.get_aggregated_order('BTC-USDT')
# print(book)
#klines = client.get_kline('BTC-USDT',1609254300, 1609164360)
#print(klines)
from kucoin.client import User
user = User(api_key, api_secret, api_passphrase, is_sandbox=True)

def returnAccountAvailable(token):
    account = user.get_account_list(token, "trade")
    return account[0]['available']

def returnPrice(token):
    account = market.get_ticker(token)
    return account['price']
#print(price)

def returnBaseMin(token):
    list = market.get_symbol_list()
    for item in list:
        if item['symbol'] == token:
            return  item['baseMinSize']

def returnIncrementSize(token):
    list = market.get_symbol_list()
    for item in list:
        if item['symbol'] == token:
            return  item['baseBaseIncrement']
from kucoin.client import Trade
client = Trade(api_key, api_secret, api_passphrase, is_sandbox=True)
# client = Trade(api_key, api_secret, api_passphrase)
# order_id = client.get_order_details('5fba98ed9def070006002197')
# order_id = client.cancel_order(self, orderId)('USDT-BTC', 'buy', size='1')
# print(order_id)
# bid = returnBid('BTC-USDT')
# order = client.create_limit_order('BTC-USDT', 'sell', 1, bid)
# print(order)

class pair(Thread):
    def __init__(self, ticker, token):
        Thread.__init__(self)
        self.ticker = ticker
        self.token = token



    def run(self):
        while (1):
            price = returnPrice(self.ticker)
            bid = returnBid(self.ticker)
            print(bid)
            available = returnAccountAvailable(self.token)
            baseMin = returnBaseMin(self.ticker)
            def amountCalculus(self, median):
                amount = .01 * randint(60, 80) * float(available) * math.exp(-abs(0.001 * (median - float(bid))))
                if float(amount) < float(baseMin):
                    amount = baseMin
                print(amount)
                return amount

            if (float(price) < medianBuy):
                debut = time.time()
                try:
                    amount = amountCalculus(self, medianBuy)
                    order = client.create_limit_order(self.ticker, 'buy', amount, bid)
                    print(f'{self.ticker}: {order}')
                    fin = time.time()
                    print(fin - debut)
                    time.sleep(randint(20, 120))
                except Exception as err:
                    print(err)
                    break
            elif (float(price) >medianSell):
                debut = time.time()
                try:
                    amount = amountCalculus(self, medianSell)
                    order = client.create_limit_order(self.ticker, 'sell', amount, bid)
                    print(f'{self.ticker}: {order}')
                    fin = time.time()
                    print(fin - debut)
                    time.sleep(randint(10, 120))
                except Exception as err:
                    print(err)
                    break

pair1 = pair('BTC-USDT','BTC')
pair2 = pair('ETH-BTC','BTC')
pair1.start()
pair2.start()
pair1.join()
pair2.join()
