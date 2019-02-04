# Constants:

stop_limit_long = 0.998

take_profit_long = 1.01 #1.01

stop_limit_short = 1.003

take_profit_short = 0.99

stddev_threshhold = 0.1 #0.05


open_count = 0

order_size = 100



class LongPosition:

    'Long position'

    def __init__(self, yes_no, entry_price, tp, sl):

        self.yes_no = yes_no
        self.entry_price = entry_price
        self.tp = tp
        self.sl = sl


class ShortPosition:

    'Short position'

    def __init__(self, yes_no, entry_price, tp, sl):

        self.yes_no = yes_no
        self.entry_price = entry_price
        self.tp = tp
        self.sl = sl


long_position = LongPosition('no', 0, 0, 0)

short_position = ShortPosition('no', 0, 0, 0)


positions_list = [['long', 'short']]


record_longs = []

record_shorts = []


def open_positions(row):

    open_date = row[0]

    entry_price = row[1]

    sl_long = entry_price * stop_limit_long   # Round this later

    tp_long = entry_price * take_profit_long

    sl_short = entry_price * stop_limit_short

    tp_short = entry_price * take_profit_short
    
    
    long_position = LongPosition('yes', entry_price, tp_long, sl_long)
   
    short_position = ShortPosition('yes', entry_price, tp_short, sl_short)
    
    positions_list_updated_row = [long_position, short_position]
    
    positions_list.append(positions_list_updated_row)
    

    record_longs_row = [open_date, entry_price, 'opened']

    record_shorts_row = [open_date, entry_price, 'opened']

    record_longs.append(record_longs_row)

    record_shorts.append(record_shorts_row)


def stopped_out_long(row):

    close_date = row[0]

    stopped_price = positions_list[-1][0].sl

    record_longs_row = [close_date, stopped_price, 'stopped']

    record_longs.append(record_longs_row)

    
    long_position = LongPosition('no', 0, 0, 0)
    
    short_position = positions_list[-1][1]
    
    positions_list_updated_row = [long_position, short_position]
    
    positions_list.append(positions_list_updated_row)
    


def stopped_out_short(row):

    close_date = row[0]

    stopped_price = positions_list[-1][1].sl

    record_shorts_row = [close_date, stopped_price, 'stopped']

    record_shorts.append(record_shorts_row)

    
 
    short_position = ShortPosition('no', 0, 0, 0)
    
    long_position = positions_list[-1][0]
    
    positions_list_updated_row = [long_position, short_position]
    
    positions_list.append(positions_list_updated_row)
    


def tp_hit_long(row):

    close_date = row[0]

    tp_price = positions_list[-1][0].tp

    record_longs_row = [close_date, tp_price, 'tp']

    record_longs.append(record_longs_row)
    
   
    long_position = LongPosition('no', 0, 0, 0)
    
    short_position = positions_list[-1][1]
    
    positions_list_updated_row = [long_position, short_position]
    
    positions_list.append(positions_list_updated_row)
    


def tp_hit_short(row):

    close_date = row[0]

    tp_price = positions_list[-1][1].tp

    record_shorts_row = [close_date, tp_price, 'tp']

    record_shorts.append(record_shorts_row)
    
  
    short_position = ShortPosition('no', 0, 0, 0)
    
    long_position = positions_list[-1][0]
    
    positions_list_updated_row = [long_position, short_position]
    
    positions_list.append(positions_list_updated_row)
    


def position_check(position_object):

    status = 'malfunction'
    
    if type(position_object) is not str:

        if position_object.yes_no == 'yes':
            status = 1
        if position_object.yes_no == 'no':
            status = 0
            
    else:
        status = 0

    return status


def signal_check(row):

    stddev_of_row = row[5]

    if stddev_of_row < stddev_threshhold:

        return 'open a straddle'

    else:
        return 'wait'




def testrun(data):
    
    open_count = 0
    longs_stopped_count = 0
    longs_hit_tp_count = 0
    shorts_stopped_count = 0
    shorts_hit_tp_count = 0
   

    for row in data:

        long_status = position_check(positions_list[-1][0])
        short_status = position_check(positions_list[-1][1])
        
        

        if long_status == 1:
            
            
            #debug_row = [row[3], positions_list[-1][0].sl ]
            #debug_list.append(debug_row)

            if row[3] < positions_list[-1][0].sl:
                stopped_out_long(row)
                longs_stopped_count += 1
                continue

            if row[2] > positions_list[-1][0].tp :
                tp_hit_long(row)
                longs_hit_tp_count += 1
                continue

        if short_status == 1:

            if row[3] > positions_list[-1][1].sl:
                stopped_out_short(row)
                shorts_stopped_count +=1
                continue

            if row[2] < positions_list[-1][1].tp:
                tp_hit_short(row)
                shorts_hit_tp_count +=1
                continue

        if long_status == 0 and short_status == 0:

            signal = signal_check(row)

            if signal == 'open a straddle':

                open_positions(row)
                
                open_count += 1
                
    
    estimated_win_long = (order_size * take_profit_long) - order_size
    estimated_loss_long = order_size - (order_size * stop_limit_long)
    estimated_win_short = order_size - (order_size * take_profit_short)
    estimated_loss_short = (order_size * stop_limit_short) - order_size
    
    estimated_wins_long_this_test = (longs_hit_tp_count * estimated_win_long)
    estimated_loss_long_this_test = longs_stopped_count * estimated_loss_long
    
    estimated_wins_short_this_test = shorts_hit_tp_count * estimated_win_short
    estimated_loss_short_this_test = shorts_stopped_count * estimated_loss_short
    
    estimated_pl_this_test = (estimated_wins_long_this_test + estimated_wins_short_this_test) - (estimated_loss_long_this_test + estimated_loss_short_this_test)

    estimated_fees_this_test = (open_count * 4) * 0.00075
    
    total_pl_after_fees = estimated_pl_this_test - estimated_fees_this_test
    
    total_risk_per_trade = (order_size - (order_size * stop_limit_long)) + ((order_size * stop_limit_short) - order_size)
    
    #results_df = pd.DataFrame(columns = ['A', 'B'])
    
    
    print('Position size per trade: ' + str(order_size))
    print('$ Risk per trade: ' + str(total_risk_per_trade))
    print(' ')
    print('Positions opened: ' + str(open_count))
    print('Longs that hit stop: ' +str(longs_stopped_count))
    print('Longs that tp: ' +str(longs_hit_tp_count))
    print('Shorts that hit stop: ' +str(shorts_stopped_count))
    print('Shorts that hit tp: ' +str(shorts_hit_tp_count))
    
    print('Total successful trades: ' + str(shorts_hit_tp_count + longs_hit_tp_count))
    
    print('Win rate: ' + str((shorts_hit_tp_count + longs_hit_tp_count) / open_count))
    
    print('Estimated P/L: ' + str(estimated_pl_this_test))
    
    print('Estimated fees: ' +str(estimated_fees_this_test))
    
    print(' ')
    
    print('Estimated P/L after fees: ' + str(total_pl_after_fees))
    
    
    
    
    
    
   
    
    #records_list = [record_longs, record_shorts]
    #return records_list
    
    return open_count, len(record_longs), longs_stopped_count, longs_hit_tp_count, shorts_stopped_count, shorts_hit_tp_count
    
                
