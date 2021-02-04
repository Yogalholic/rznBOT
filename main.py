import time
from threading import Thread
from random import seed
from random import randint
import math
from decimal import Decimal
seed(2)
medianBuy = #upper limit price to execute buying orders
medianSell = #lower limit price to execute selling orders

#  MarketData
from kucoin.client import Market
client = Market(url='https://api.kucoin.com')
#client = Market()

# or connect to Sandbox
#market = Market(url='https://openapi-sandbox.kucoin.com')
#market = Market(is_sandbox=True)
api_key = ''
api_secret = ''
api_passphrase = ''
def returnBid(symbol):
    '''
    :param symbol: a trading pair ('BTC-USDT',...)
    :return:  the second bid in the order book
    '''
    book = Market.get_aggregated_order(symbol)
    return book['bids'][1][0]

# User
from kucoin.client import User
client = User(api_key, api_secret, api_passphrase)

# or connect to Sandbox
#user = User(api_key, api_secret, api_passphrase, is_sandbox=True)

def returnAccountAvailable(currency):
    '''
    :param currency: a symbol of a currency ('BTC', 'ETH',...)
    :return: Funds available to withdraw or trade
    '''
    account = User.get_account_list(currency, "trade")
    return account[0]['available']

def returnPrice(symbol):
    '''
    :param symbol: a trading pair ('BTC-USDT',...)
    :return: the last deal price of a trading pair
    '''
    account = Market.get_ticker(symbol)
    return account['price']

def returnBaseMin(symbol):
    '''
    :param symbol: a trading pair ('BTC-USDT',...)
    :return: The minimum order quantity required to place an order
    '''
    liste = Market.get_symbol_list()
    element = list(filter(lambda item: item['symbol'] == symbol, liste))
    return element[0]['baseMinSize']

def returnIncrementSize(symbol):
    '''
    :param symbol: a trading pair ('BTC-USDT',...)
    :return: The increment of the order size.
    '''
    liste = Market.get_symbol_list()
    element = list(filter(lambda item: item['symbol'] == symbol, liste))
    return Decimal(element[0]['baseIncrement'])

# Trade
from kucoin.client import Trade
client = Trade(api_key, api_secret, api_passphrase)

# or connect to Sandbox
# client = Trade(api_key, api_secret, api_passphrase, is_sandbox=True)
class pair(Thread):
    def __init__(self, symbol, currency):
        Thread.__init__(self)
        self.symbol = symbol
        self.currency = currency



    def run(self):
        while (1):
            price = returnPrice(self.symbol)
            bid = returnBid(self.symbol)
            print(f'bid: {bid}')
            available = returnAccountAvailable(self.currency)
            baseMin = returnBaseMin(self.symbol)
            baseIncrement = returnIncrementSize(self.symbol)
            def amountCalculus(self, median):
                '''
                :param self: instance of a thread of a trading pair
                :param median: the median price of a trading pair
                :return:  size of the order calculated as a percentage of funds available and following an exponential decay
                '''
                amount = Decimal(.01 * randint(60, 80) * float(available) * math.exp(-abs(0.001 * (median - float(bid)))))
                amount = Decimal(amount).quantize(baseIncrement)
                if float(amount) < float(baseMin):
                    amount = baseMin
                print(f'amount: {amount}')
                return amount

            def executeOrder(self, orderSide):
                '''
                :param self: instance of a thread of a trading pair
                :param orderSide: buy or sell
                :return: JSON of the order
                '''
                amount = amountCalculus(self, medianBuy)
                return client.create_limit_order(self.symbol, orderSide, float(amount), bid)


            if (float(price) < medianBuy):
                try:
                    order = executeOrder(self, 'buy')
                    print(f'{self.symbol}: {order}')
                    time.sleep(randint(20, 120))
                except Exception as err:
                    print(err)
                    break
            elif (float(price) >medianSell):
                try:
                    order = executeOrder(self, 'sell')
                    print(f'{self.symbol}: {order}')
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
