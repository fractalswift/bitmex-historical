#!/usr/bin/env python3

import pandas as pd
import bitmex_history_downloader as bhd
pd.set_option("display.precision", 9)
import time

print('Lets go!')

tickers_list = ['.BEOSXBT', '.BADAXBT', '.BBCHXBT', 'ETHUSD', '.BLTCXBT', '.TRXXBT', '.BXRPXBT', 'XBTUSD']

for ticker in tickers_list:
    
    try:
    
        df = pd.read_pickle('new_pickles/' + ticker[1:])

        save_path = 'new_pickles/' + str(ticker[1:])

        print('File opened, making first 150 api calls now...')

        df = bhd.make_150_update_api_calls(df)

        df.to_pickle(save_path)

        print('saved...')

        time.sleep(310)

        df = bhd.make_150_update_api_calls(df)

        df.to_pickle(save_path)

        print('saved...')

        time.sleep(310)

        df = bhd.make_150_update_api_calls(df)

        df.to_pickle(save_path)

        print('saved...')

        time.sleep(310)

        df = bhd.make_150_update_api_calls(df)

        df.to_pickle(save_path)

        print('saved...')

        time.sleep(310)

        df = bhd.make_150_update_api_calls(df)

        df.to_pickle(save_path)

        print('saved...')

        time.sleep(310)

        df = bhd.make_150_update_api_calls(df)

        df.to_pickle(save_path)

        print('saved...')

        time.sleep(310)

        df = bhd.make_150_update_api_calls(df)

        df.to_pickle(save_path)

        print('saved...')

        time.sleep(310)

        df = bhd.make_150_update_api_calls(df)

        df.to_pickle(save_path)

        print('saved...')

        time.sleep(310)

        df = bhd.make_150_update_api_calls(df)

        df.to_pickle(save_path)

        print('saved...')

        time.sleep(310)

        df = bhd.make_150_update_api_calls(df)

        df.to_pickle(save_path)

        print('saved...')

        time.sleep(310)

        df = bhd.make_150_update_api_calls(df)

        df.to_pickle(save_path)

        print('saved...')

        time.sleep(310)

        df = bhd.make_150_update_api_calls(df)

        df.to_pickle(save_path)

        print('saved...')

        time.sleep(310)

        df = bhd.make_150_update_api_calls(df)

        df.to_pickle(save_path)

        print('saved...')

        time.sleep(310)

        df = bhd.make_150_update_api_calls(df)

        df.to_pickle(save_path)

        print('saved...')

        time.sleep(310)

        df = bhd.make_150_update_api_calls(df)

        df.to_pickle(save_path)

        print('saved...')

        time.sleep(310)

        df = bhd.make_150_update_api_calls(df)

        df.to_pickle(save_path)

        print('saved...')

        time.sleep(310)

        df = bhd.make_150_update_api_calls(df)

        df.to_pickle(save_path)

        print('saved...')

        time.sleep(310)

        df.to_pickle(save_path)

        print('I have completed and saved ' + ticker)

        time.sleep(310)

    except Exception:
        print('Skipped this one for some reason')
        pass
    
    
    
    
    
    
    
