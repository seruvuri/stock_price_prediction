# Stock Price Predicition (For 100 days)


# Project Overview

***Brief:***-  Getting stocks data From :https://api.tiingo.com/ and performing EDA and Feature Engineering on data, using LSTM(Long Shot-Term Memory) technique for predicting stock for n number of days.

![image](https://github.com/seruvuri/stock_price_prediction/assets/109864276/cbb3de27-ad64-41a6-addb-2f1638821448)


## Dataset Description

>Date:    The date this data pertains to.

>Open:    The opening price for the asset on the given date.

>High:    The high price for the asset on the given date.

>Low:     Low proce for theasset on the given date

>close:   closing proce for the asset on given date.

>Volume:  The number of shares traded on IEX only.



## Data Ingestion

![image](https://github.com/seruvuri/stock_price_prediction/assets/109864276/92bafa4c-3b96-44dd-a4e7-f39b0827af84)

  Using TIINGO api https://www.tiingo.com/documentation/general/overview to extract stock data  

***API's***

  >For ticker meta data : **https://api.tiingo.com/tiingo/fundamentals/meta?token={}**
  
  >For Ticker stock details : **https://api.tiingo.com/iex/{}/prices?startDate={}&resampleFreq={}&columns=open,high,low,close,volume&token={}**

API parameter's description:

    ticker name = stock name in tiingo website
    
    Start Date = Date from when we need historical data of a stock(format YYYY-MM-DD)
    
    resampleFreq = This allows you to set the frequency in which you want data resampled. 
                    
                    For example "1hour" would return the data where OHLC is calculated on an hourly schedule.

## Data Transformation

> Checking NULL values

>Data Scaling:
    ***LSTM are sensitive to the scale of data. So we apply "MinMax scaler"***

>Splitting data into test and train

>Creating dataset for LSTM model input
