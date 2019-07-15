# bitmex-historical

Simple Python script for automatically downloading historical data from bitmex


Bitmex_history_downloader is a simple mini module for downloading any historical trades on the Bitmex API. It does not require authentication. It can be used easily in Jupyter notebook.
  
Installation:
    The module is not available on pip. Simply cut and paste the code from the repository to your workspace and name it bitmex_history_downloader.py
    
 Dependencies:
 
      Requires the following packages: requests, pandas, numpy, bitmex, datetime (including timedelta), time.
      All of the above modules can be installed with pip
      
 
Usage:
 
Steps to download historical data:

1. import the module:

         import bitmex_history_downloader as bhd


2. create the first dataframe:

        bhd.make_base_sheet(coinpair, resolution, start_time, end_time)

Please note you must specify an end time that is more than 4 rows away from the start time. E.g if you are using 1d resolution you will need to set the dates for the base sheet at least 4 days apart. To be economical with your rate-limit usage, set them to be about 750 rows apart (this is max rows allowed by bitmex per call).

Example:

        import bitmex_history_downloader as bhd
  
        df = bhd.make_base_sheet('ETHUSD', '1m', '2018-12-01 00:00:00', '2018-12-30 12:30:00')

 Bitmex accepts the follwing resolutions: '1m', '5m' '1h', '1d'
    
Bitmex accepts the following coinpairs: '.BEOSXBT', '.BADAXBT', '.BBCHXBT', 'ETHUSD', '.BLTCXBT', '.TRXXBT', '.BXRPXBT', 'XBTUSD'
    
Please note the altcoins ending in XBT (e.g .BADAXBT) represent the index, not the historical trades. If you wish to get the historical trades you must replace them with the contract you with, e.g ADAU18. Please remember to use the correct start and end period as these contracts have a start and expirey date.

If you already have some bitmex historical data (it must be saved in bitmex format) e.g you haved used bitmex_history_downloader before and saved the results to csv, you can just import from your csv:

        df = pd.read_csv('YOUR_PREVIOUS_DATA.csv')


3. use the update function to bring the file up to present date:

        df = bdh.make_150_api_update_calls(df)

Important: if timestamp object is a string, it won't work. It needs to be a datetime object. If you have imported from csv you will need to convert this first

Please note: This function actually makes 148 calls so that you don't accidentally max out if using directly after the base sheet.

This updates only 148 x 750 rows (so 111000 minutes (78 days) if on 1m resolution, or 555000 minutes (1 year) on 5m resolution etc).

The function will automatically detect the coinpair and the resolution of your previous sheet (remember it must be the bitmex api format).

YOU MUST WAIT 5 MINUTES BEFORE RUNNING AGAIN or you will trigger an IP ban from bitmex as they rate-limit to 150 requests/5 min. You may use a sleep loop using the time module.


4. Save your data as a csv file

          df.to_csv('YOUR_CHOSEN_FILENAME.csv')

If you do this step then you can update your data whenever you want, just go back to step 2 with this data. 

AUTOMATED SOLUTION: If you want to download a lot of data and do not want to wait around in front of your computer, please run automatic_bhd.py from command line.
    
