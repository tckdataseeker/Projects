''' 
The following code should be run on a Jupyter notebook.
The following helps you execute a strangle options strategy using Robinhood APIs
'''
import robin_stocks as r
from robin_stocks import *
import pandas as pd
import sched, time
import numpy as np
import threading
from time import sleep
from datetime import datetime

# cell #1
login = r.login('[enter your username]','[enter your password]')

# cell #2
symbol = input('Stock symbol: ').upper()
expiration = input('expiration_date: ')

#cell #3
# identify the options you want to have as your strangle legs - you're not buying by running this code

keys = ['adjusted_mark_price','delta','gamma','theta']
stock = symbol
date = expiration
call_strike_price = 115 #enter your call strike price here
put_strike_price = 97.5 #enter your put strike price here

call = r.options.find_options_by_expiration_and_strike(stock,date,str(call_strike_price),optionType = 'call')[0]
print([stock, [call[x] for x in keys]]) # get the price of the stock, delta, gamma, and theta of the call option
put = r.options.find_options_by_expiration_and_strike(stock,date,str(put_strike_price),optionType = 'put')[0]
print([stock, [put[x] for x in keys]]) # get the price of the stock, delta, gamma, and theta of the put option


#cell #4
# adjust mark price for option that are priced above $3
if float(call['adjusted_mark_price']) >= 3:
    call['adjusted_mark_price'] = np.round(np.floor(float(call['adjusted_mark_price'])/.05)*.05,2)

if float(put['adjusted_mark_price']) >= 3:
    put['adjusted_mark_price'] = np.round(np.floor(float(put['adjusted_mark_price'])/.05)*.05,2)

#cell #5
'''
Execute the strangle, define the capital you want to put in for EACH leg. 
Your total capital will be approximately double the capital you input 
'''

capital_per_option = 1000

strangle_call_leg = r.orders.order_buy_option_limit('open', 'debit', float(call['adjusted_mark_price'])
                                                    , call['chain_symbol']
                                           , np.floor(np.floor(capital_per_option/float(call['adjusted_mark_price']))/100)
                                                    , call['expiration_date'], 
                                                   float(call['strike_price']), optionType='call', timeInForce='gtc')

strangle_put_leg = r.orders.order_buy_option_limit('open', 'debit', float(put['adjusted_mark_price'])
                                                   , put['chain_symbol']
                                           , np.floor(np.floor(capital_per_option/float(put['adjusted_mark_price']))/100)
                                                   , put['expiration_date'], 
                                                   float(put['strike_price']), optionType='put', timeInForce='gtc')