import os,sys
from src.exception import CustomException
from src.logger import logging
import requests
import dill


'''
ticker name= stock name in tiingo website
Start Date= Date from when we need historical data of a stock(format YYYY-MM-DD)
resampleFreq = This allows you to set the frequency in which you want data resampled. For example "1hour" would return the data where OHLC is calculated on an hourly schedule.

'''

#geeting ticker deatils form tiingo 
def ticker_details(token):
    try:
        
        logging.info("Getting ticker deatails from website")
        meta_url="https://api.tiingo.com/tiingo/fundamentals/meta?token={}".format(token)
        ticker=requests.get(meta_url)
        status=ticker.status_code
        if status==200:
            logging.info('Conneciton established successfully with status code {status_code}'.format(' ',status_code=status))
            ticker_df=ticker.json()
            
            return ticker_df
                    
        elif status in [400,500,401,502,404]:
            logging.info('unable to establish connection. error code {status_code}'.format(status_code=status))

    except Exception as e:
        raise CustomException(e,sys)
    
#geeting Stock deatils form tiingo 
    
def api_data_extraction(ticker_name,startDate,resampleFreq,token):
    try:
        logging.info('connecting to "TIINGO" website using api to fetch "{ticker_details}" stock data'.format('',ticker_details=ticker_name))
        tiingo_api_url="https://api.tiingo.com/iex/{}/prices?startDate={}&resampleFreq={}&columns=open,high,low,close,volume&token={}".format(ticker_name,startDate,resampleFreq,token)


        data=requests.get(tiingo_api_url)
        status=data.status_code

        if status==200:
            logging.info('Conneciton established successfully with status code {status_code}'.format(' ',status_code=status))
            dataset=data.json()
            logging.info('Data Extraction is Succesfully ')
            return dataset
        elif status in [400,500,401,502,404]:
            logging.info('unable to establish connection. error code {status_code}'.format(status_code=status))
    except Exception as e:
        raise CustomException(e,sys)

def save_obj(file_path, obj):
    try:
        dir_path=os.path.dirname(file_path)

        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e,sys)