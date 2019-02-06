import csv
import pandas as pd
import datetime as dt
import bitmex
import requests
import json

# Variables and functions:


record_row = []

time_of_script_execution = str(dt.datetime.now())

record_row.append(time_of_script_execution)


take_profit_long = 1.01
take_profit_short = 0.99

stop_limit_long = 0.998
stop_limit_short = 1.002


client_long = bitmex.bitmex(
    test=True,
    api_key="O_lodCc7sDZ9n7yZJQFZPOpH",
    api_secret="voJivpHQ-6QxFu_9C3gaKofGTMjvHiu48SbA5Q5QBIXnBicE"
)


client_short = bitmex.bitmex(
    test=True,
    api_key="gvc3Vvl1PUxwYE0zSsqZYhmH",
    api_secret="WjHaURtQbn-T0X6bd3CugXxGzRTjh7ZycLultQY0nSkdCyco"
)


positions_long = client_long.Position.Position_get(filter=json.dumps({'symbol': 'XBTUSD'})).result()

positions_short = client_short.Position.Position_get(filter=json.dumps({'symbol': 'XBTUSD'})).result()





order_size = 10


def check_for_orders_long_client(client_id):
    
        orders = client_id.Order.Order_getOrders(filter=json.dumps({"open": True})).result()
        
        
        try:
            order_1_type = orders[0][0].get('ordType')
            order_1_side = orders[0][0].get('side')
            order_1_details = [order_1_type, order_1_side]
        except Exception: 
            order_1_type = 'No order 1'
            order_1_details = ['No order 1', 'No order 1']


        try:
            order_2_type = orders[0][1].get('ordType')
            order_2_side = orders[0][1].get('side')
            order_2_details = [order_2_type, order_2_side]

        except Exception: 
            order_2_type = 'No order 2'
            order_2_details = ['No order 2', 'No order 2']

        try:
            order_3_type = orders[0][2].get('ordType')
            order_3_side = orders[0][2].get('side')
            order_3_details = [order_3_type, order_3_side]
        except Exception: 
            order_3_type = 'No order 3'
            order_3_details = ['No order 3', 'No order 3']



        orders_list = [order_1_details, order_2_details, order_3_details]

        current_orders = []

        for order in orders_list:
            if order[0] == 'Limit' and order[1] == 'Sell':
                current_orders.append('Take profit')
            if order[0] == 'Limit' and order[1] == 'Buy':
                current_orders.append('Limit buy')
            if order[0] == 'Stop' and order[1] == 'Sell':
                current_orders.append('Stop')

        return current_orders
    
    
    
def check_for_orders_short_client(client_id):
    
        orders = client_id.Order.Order_getOrders(filter=json.dumps({"open": True})).result()
        
        
        try:
            order_1_type = orders[0][0].get('ordType')
            order_1_side = orders[0][0].get('side')
            order_1_details = [order_1_type, order_1_side]
        except Exception: 
            order_1_type = 'No order 1'
            order_1_details = ['No order 1', 'No order 1']


        try:
            order_2_type = orders[0][1].get('ordType')
            order_2_side = orders[0][1].get('side')
            order_2_details = [order_2_type, order_2_side]

        except Exception: 
            order_2_type = 'No order 2'
            order_2_details = ['No order 2', 'No order 2']

        try:
            order_3_type = orders[0][2].get('ordType')
            order_3_side = orders[0][2].get('side')
            order_3_details = [order_3_type, order_3_side]
        except Exception: 
            order_3_type = 'No order 3'
            order_3_details = ['No order 3', 'No order 3']



        orders_list = [order_1_details, order_2_details, order_3_details]

        current_orders = []

        for order in orders_list:
            if order[0] == 'Limit' and order[1] == 'Buy':
                current_orders.append('Take profit')
            if order[0] == 'Limit' and order[1] == 'Sell':
                current_orders.append('Limit sell')
            if order[0] == 'Stop' and order[1] == 'Buy':
                current_orders.append('Stop')

        return current_orders   
  



orders_long_acc = check_for_orders_long_client(client_long)
orders_short_acc = check_for_orders_short_client(client_short)



current_long_avg_bought_at = positions_long[0][0].get('avgEntryPrice')

current_short_avg_sold_at = positions_short[0][0].get('avgEntryPrice')


def place_tp_long(client_id):
    

                current_avg_bought_at = positions_long[0][0].get('avgEntryPrice')
            
                
            
                
                response = client_id.Order.Order_new(
                    symbol="XBTUSD",
                    side="Sell",
                    orderQty=long_positions,
                  
                    price=round(  (current_avg_bought_at * take_profit_long) * 2.0 ) /2.0 ,
                    execInst= 'ParticipateDoNotInitiate'
                ).result()
                
                tp_set_at = round(   (current_avg_bought_at * take_profit_long) * 2.0 ) /2.0

                return tp_set_at
            
           
                
                
            
def place_tp_short(client_id):
    
            
                current_avg_sold_at = positions_short[0][0].get('avgEntryPrice')
            
           
                response = client_id.Order.Order_new(
                    symbol="XBTUSD",
                    side="Buy",
                    orderQty= -(short_positions),
                  
                    price=round(  (current_avg_sold_at * take_profit_short) * 2.0 ) /2.0 ,
                    execInst= 'ParticipateDoNotInitiate'
                ).result()
                
           
                
                
                tp_set_at = round(   (current_avg_sold_at * take_profit_short) * 2.0 ) /2.0

                return tp_set_at
            
          
            
            
short_positions = positions_short[0][0].get('currentQty')
long_positions = positions_long[0][0].get('currentQty')


# The strategy - In reality it should check the charts and generate a 1 or 0

always_straddle_strategy = 1 

def open_long_at_market(client_id_long):
    
    long_response = client_id_long.Order.Order_new(
                    symbol="XBTUSD",
                    side="Buy",
                    orderQty= order_size,
                    ordType="Market"
                ).result()
    
def open_short_at_market(client_id_short):
    
    long_response = client_id_short.Order.Order_new(
                    symbol="XBTUSD",
                    side="Sell",
                    orderQty= order_size,
                    ordType="Market"
                ).result()
    
    
def place_stop_for_long(client_id_long): 
    
                     client_id_long.Order.Order_new(
                                symbol="XBTUSD",
                                side="Sell",
                                ordType='Stop',
                                stopPx= round( (current_long_avg_bought_at * stop_limit_long) * 2.0 )/ 2.0,   # Might need to be string
                                orderQty=order_size,
                            ).result()
        
def place_stop_for_short(client_id_short): 
    
                     client_id_short.Order.Order_new(
                                symbol="XBTUSD",
                                side="Buy",
                                ordType='Stop',
                                stopPx= round( (current_short_avg_sold_at * stop_limit_short) * 2.0 )/ 2.0,   # Might need to be string
                                orderQty=order_size,
                            ).result()
        

always_straddle_strategy = 1 # In reality it should check the charts and generate a 1 or 0

def check_signal(strategy):
    
    if strategy == 1:
        
        return 1
    
    if strategy == 0:
        
        return 0

signal = check_signal(always_straddle_strategy)



def open_straddle(client_id_long, client_id_short):
    
    # Open the long order
    
    open_long_at_market(client_long)
    
    
    # Open the short order
    
    open_short_at_market(client_short)
    
    
    # Check to see if I have a stop for the long (could be an old stop):
    
    orders_long_acc = check_for_orders_long_client(client_long)
    
    # If no stop, place one:
    
    if 'Stop' not in orders_long_acc: 
                            
                          place_stop_for_long(client_long)
                
    
    # If stop, amend it (because if I am in this part of the code, I must be placing an new position, so it must be an old stop)
    
    elif 'Stop' in orders_long_acc:
                            
                            # Get stop ID and amend it
                            
                            amend_stop_long(client_long)
                        
                        
    # Check to see if I have a stop for the short (could be an old stop):
    
    
    orders_short_acc = check_for_orders_short_client(client_short)
    
    # If no stop, place one:
    
    if 'Stop' not in orders_short_acc: 
                            
                          place_stop_for_short(client_short)
                
     
    # If stop, amend it (because if I am in this part of the code, I must be placing an new position, so it must be an old stop)
    
    elif 'Stop' in orders_short_acc:
                            
                            # Get stop ID and amend it
                            
                            amend_stop_short(client_short)
                        
                        


# Main bot logic :


# Below checks if I have positions so I can add tp. Though this could technically happen as part of 

# open_straddle (since it is market), it is possible that market won't have filled yet so this allows 15s

# to avoid annoying errors caused by that




# Step 1: Check position status

if long_positions > 0 and short_positions == 0:
    
    record_row.append('A long is still open but a short has closed')
    
if short_positions < 0 and long_positions == 0:
    
    record_row.append('A short is still open but a long has closed')
    
   
    
 
       
# Step 2: If we have positions without tps, add a tp. Technically could do this in open_straddle, but doing it here

# allows the length of loop (15s) for straddle market orders to fill and avoid errors

if long_positions > 0:
    
    orders = orders_long_acc
    
    if 'Take profit' not in orders:
        
        tp = place_tp_long(client_long)
        
        
        record_row.append('Got long filled, setting tp at ' + str(tp))
        
    else:
        record_row.append('Already had filled long and tp in place, doing nothing')


if short_positions < 0:
    
    orders = orders_short_acc
    
    if 'Take profit' not in orders:
        tp = place_tp_short(client_short)
        
        
        record_row.append('Got short filled, setting tp at ' + str(tp))
    
    else:
        record_row.append('Already had filled short and tp in place, doing nothing')
        


# Below checks if I have no postions. This can only happen after a staddle trade as been closed completetly.

# Therefore it is always time to open an new one (if signal confirms)
        

if long_positions == 0 and long_positions == 0:
    
    # Check for signal - it will always be to open in this example

    if signal == 1:
        
        entry_prices = open_straddle(client_long, client_short)
        
        record_row.append('Opened a new straddle trade')
        
    elif signal == 0:
        
        record_row.append('Have no positions open, waiting for signal')



elif long_positions > 0 and long_positions < 0:
    
    record_row.append('Both halves of straddle are still open and stops and tp are in place')
    
    
print(record_row)
        
    
    
    
