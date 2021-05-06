import finplot as fplt
import yfinance as yf
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as web
import math
from pandas_datareader import data
from matplotlib.ticker import FuncFormatter
from matplotlib import style


action=True
#setting the day of today and day of six_months_before
today=datetime.today().strftime('%Y-%m-%d')
six_months_before= date.today() + relativedelta(months=-6)

#keep the action continue by action=True
while action==True:

    # User enter number to select the function they want to use
    choice=eval(input("1. Candlestick Plot\n2. Mean Return\n3. Standard Deviation\n4. Correlation of Portfolio\n5. Weight of two stock\n6. Buy and Shortsale timing\n7. Monte Carlo Simulation for AAPL and TSM\n8. Quit Program\n"+"Please select your action by entering a number from 1 to 8: "))

    if choice == 1: #Candlestick Plot

        #collect data from yahoo finance
        ticker = input('Please input the ticker for Candlestick Plot:')
        data = web.get_data_yahoo(ticker,
                                  start=six_months_before,
                                  end=today)

        #create candlestick plot
        ax = fplt.create_plot(ticker)
        fplt.candlestick_ochl(data[['Open', 'Close', 'High', 'Low']], ax=ax)

        # create SMA 10, SMA 25, SMA 50
        fplt.plot(data.Close.rolling(10).mean(), ax=ax, legend='SMA 10')
        fplt.plot(data.Close.rolling(25).mean(), ax=ax, legend='SMA 25')
        fplt.plot(data.Close.rolling(50).mean(), ax=ax, legend='SMA 50')

        # showing the graph
        fplt.show()

    elif choice == 2:#Mean Return

        # collect data from yahoo finance
        ticker = input('Please input the ticker for Mean Return:')
        data = web.get_data_yahoo(ticker,
                                  start=six_months_before,
                                  end=today)['Adj Close']

        #find daily pecentage change of stock
        daily_returns = data.pct_change()
        # find mean return
        print('Mean ruturn is '+ daily_returns.mean())

    elif choice == 3:

        # collect data from yahoo finance
        ticker = input('Please input the ticker for Standard Deviation:')
        data = web.get_data_yahoo(ticker,
                                  start=six_months_before,
                                  end=today)['Adj Close']

        # find daily pecentage change of stock
        daily_returns = data.resample('D').ffill().pct_change()

        # find the variance and get the Standard Deviation
        variance = np.var(daily_returns, ddof=1)
        Standard_Deviation = math.sqrt(variance)

        print('Standard_Deviation is '+Standard_Deviation)


    elif choice == 4:
        tickers = []

        # Let user input number of stock they want into portfolio
        n = int(input("How many tickers you want to input : "))
        for i in range(0, n):
            content = input('Input the tickers one by one for correlation:')
            tickers.append(content)

        # collect data from yahoo finance
        profoilo = web.get_data_yahoo(tickers,
                                      start=six_months_before,
                                      end=today)['Adj Close']

        # find daily pecentage change of stock
        profoilo_daily_returns = profoilo.pct_change()

        # find the portfolio correlation
        print(profoilo_daily_returns.corr())


    elif choice == 5:
        tickers = []
        #allow user input two tickers
        n = 2
        for i in range(0, n):
            content = input('Input the two tickers one by one for weight:')
            tickers.append(content)
        # collect data from yahoo finance
        profoilo = web.get_data_yahoo(tickers,
                                      start=six_months_before,
                                      end=today)['Adj Close']
        #find the corretation
        Return = np.log(profoilo / profoilo.shift(1))
        Correlation = Return.cov()

        # Simulating every date in profoilo
        daycount = 1000
        # Creating an empty array to store portfolio weights
        AllWeight = np.zeros((daycount, len(profoilo.columns)))
        # Creating an empty array to store portfolio risks
        PortfolioRisk = np.zeros((daycount))

        #simulate the portfolio returns and risk
        for i in range(daycount):
            #generate random weight
            weight = np.random.uniform(size=len(profoilo.columns))
            weight = weight / np.sum(weight)

            # saving weights in the array
            AllWeight[i, :] = weight

            # Portfolio Risk (compare sd and compare var will have same result)
            StandardDeviation = np.sqrt(np.dot(weight.T, np.dot(Correlation, weight)))
            PortfolioRisk[i] = StandardDeviation

        # find to minimum variance
        Minimum_Variance = AllWeight[PortfolioRisk.argmin()]

        #transfer minimum variance to 2 decimal places
        StockWeight = []
        for item in Minimum_Variance:
            StockWeight.append("%.2f" % item)

        print("Stock Weight of ticker1 and ticker2:", StockWeight)

    elif choice == 6:

        # collect data from yahoo finance
        ticker = input('Please input the ticker for Candlestick Plot:')
        data = web.get_data_yahoo(ticker,
                                start=six_months_before,
                                end=today)
        #calculate the SMA
        data['SMA10']=data['Adj Close'].rolling(10).mean()
        data['SMA25']=data['Adj Close'].rolling(25).mean()
        
        #add SMA in to data dataset
        data=data[['Adj Close','SMA10','SMA25']]
        data=data.dropna()

        #Find the buy and Shortsale timing by compare two day different of SMA10 and SMA25
        Buy=[]
        Shortsale=[]

        for i in range(len(data)):
            if data.SMA10.iloc[i]>data.SMA25.iloc[i] and data.SMA10.iloc[i-1]<data.SMA25.iloc[i-1]:
                Buy.append(i)
            elif data.SMA10.iloc[i]<data.SMA25.iloc[i] and data.SMA10.iloc[i-1]>data.SMA25.iloc[i-1]:
                Shortsale.append(i)

        #Create the graph
        plt.plot(data['SMA10'], label= 'SMA10' , c='k', alpha= 0.9 )
        plt.plot(data['SMA25'], label='SMA25', c='magenta', alpha=0.9)
        plt.plot(data['Adj Close'], label='Asset_Price', c='blue', alpha=0.5)
        plt.scatter(data.iloc[Buy].index,data.iloc[Buy]['Adj Close'],marker='^',c='g',s=100)
        plt.scatter(data.iloc[Shortsale].index, data.iloc[Shortsale]['Adj Close'], marker='v', c='r', s=100)

        #show the label and pop out graph
        plt.legend()
        plt.show()


    elif choice == 7:

        # getting Apple and tsm stock prices from yahoo
        prices = web.DataReader('AAPL', 'yahoo', six_months_before, today)['Adj Close']
        prices2 = web.DataReader('TSM', 'yahoo', six_months_before, today)['Adj Close']

        # getting returns
        returns = prices.pct_change()
        last_price = prices[-1]

        returns2 = prices2.pct_change()
        last_price2 = prices2[-1]

        # simulation times
        num_simulations = 20

        #number of trading day of next month
        trading_days = 21

        # set a dataframe for simulation results
        sim_data = pd.DataFrame()

        for x in range(num_simulations):

            count = 0
            #find SD of stock
            daily_vol = returns.std()
            daily_vol2 = returns2.std()

            price_series = []

            # start the simulation
            for i in range(trading_days):
                if count == 20:
                    break

                #weight can be found in function 5 of this program
                price = last_price * (
                        0.68 * math.exp(returns.mean() + daily_vol * np.random.normal())) + last_price2 * (
                        0.32 * math.exp(returns2.mean() + daily_vol2 * np.random.normal()))
                price_series.append(price)
                count += 1


            sim_data[x] = price_series
        #turn every day return into pecentage
        test = sim_data.pct_change()

        #initial investment money put in the portfolio after one month of trading day
        AfterOneMonth = 1000000 * (1 + test)

        #Covert to rate of return
        RateOfReturn = (AfterOneMonth.iloc[-1] - 1000000) / 1000000
        print(RateOfReturn)

    elif choice == 8:

            print('See you next time!')
            #stop the while loop
            action = False








