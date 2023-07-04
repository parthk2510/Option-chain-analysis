import subprocess
import time
import pymongo
from pymongo import MongoClient
import math
from scipy import optimize
from datetime import datetime

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["mydatabase"]
collection = db["mycollection"]

# Define a helper function to store variables in MongoDB
def store_variables_in_mongodb(variables):
    collection.insert_one(variables)

command = 'java -Ddebug=true -Dspeed=4.0 -classpath ./feed-play-1.0.jar hackathon.player.Main dataset1.csv 9011'

# Execute the command
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Process the output in a loop
while True:
    # Read one line at a time from the output
    line = process.stdout.readline()
    if not line:
        # No more output, break out of the loop
        break
    
    if "Publishing MarketData" in line:
        # Perform processing on the line
        data = line.split("=")
        symbol = data[1].split(",")[0]
        LTP = data[2].split(",")[0]
        LTQ = data[3].split(",")[0]
        totalTradedVolume = data[4].split(",")[0]
        bestBid = data[5].split(",")[0]
        bestAsk = data[6].split(",")[0]
        bestBidQty = data[7].split(",")[0]
        bestAskQty = data[8].split(",")[0]
        openInterest = data[9].split(",")[0]
        timestamp = data[10].split(",")[0]
        sequence = data[11].split(",")[0]
        prevClosePrice = data[12].split(",")[0]
        prevOpenInterest = data[13].split(",")[0].replace("}","")
        if symbol[1]=='M':
            if(len(symbol)==9):
                date = ''
                option = ''
                strikePrice = 0
                symbol = symbol[0:8]
            else:
                date = symbol[8:15]
                option = symbol[len(symbol)-3:len(symbol)-1]
                strikePrice = symbol[15:len(symbol)-3]
                symbol = symbol[0:8]
                
        if symbol[1]=='F':
            if(len(symbol)==12):
                date = ''
                option = ''
                strikePrice = 0
                symbol = symbol[1:11]
            else:
                date = symbol[11:18]
                option = symbol[len(symbol)-3:len(symbol)-1]
                strikePrice = symbol[18:len(symbol)-3]
                symbol = symbol[1:11]
        if symbol[1]=='A':
            if(len(symbol)==10):
                date = ''
                option = ''
                strikePrice = 0
                symbol = symbol[1:9]
            else:
                date = symbol[9:16]
                option = symbol[len(symbol)-3:len(symbol)-1]
                strikePrice = symbol[16:len(symbol)-3]
                symbol = symbol[1:9]
        symbol = symbol.replace("'","")
        LTP = float(LTP)
        LTQ = int(LTQ)
        strikePrice = float(strikePrice)
        totalTradedVolume = int(totalTradedVolume)
        bestBid = float(bestBid)
        bestAsk = float(bestAsk)
        bestBidQty = int(bestBidQty)
        bestAskQty = int(bestAskQty)
        openInterest = int(openInterest)
        sequence = int(sequence)
        prevClosePrice = float(prevClosePrice)
        prevOpenInterest = float(prevOpenInterest)
        changeInOi = openInterest-prevOpenInterest
        priceChange = LTP-prevClosePrice

        def IV(LTP, strikePrice, date):

            # Define the Black-Scholes formula for calculating the options price
            def black_scholes(iv, S, strikePrice, r, ttm):
                d1 = (math.log(S / strikePrice) + (r + 0.5 * iv ** 2)
                      * ttm) / (iv * math.sqrt(ttm))
                d2 = d1 - iv * math.sqrt(ttm)
                call_price = S * \
                    norm_cdf(d1) - strikePrice * \
                    math.exp(-r * ttm) * norm_cdf(d2)
                return call_price

            # Define the cumulative distribution function (CDF) of the standard normal distribution
            def norm_cdf(x):
                return (1 + math.erf(x / math.sqrt(2))) / 2

            # Function to calculate the difference between the calculated and observed options prices
            def price_difference(iv, LTP, S, strikePrice, r, ttm):
                calculated_price = black_scholes(iv, S, strikePrice, r, ttm)
                return calculated_price - LTP

            # Function to calculate the Implied Volatility (IV) using optimization
            def calculate_iv(LTP, S, strikePrice, r, ttm):
                # Set the initial guess for IV
                initial_guess = 0.5

                # Use optimization to find the value of IV that minimizes the price difference
                result = optimize.root(
                    price_difference, initial_guess, args=(LTP, S, strikePrice, r, ttm))
                iv = result.x[0]
                return iv

            expiration_date = datetime.strptime(date, "%d%b%y")
            current_date = datetime.now()
            ttm = (expiration_date - current_date).days / 365
            # Example usage
            # Observed options price
            S = 19322.55  # Underlying price
            # Strike price
            r = 0.1  # Risk-free interest rate
            iv = calculate_iv(LTP, S, strikePrice, r, ttm)
            return iv
        # if sequence > 4:
        #     iv = IV(LTP, strikePrice, date)
        # else:
        #     iv = 0


        variables = {
            "symbol": symbol,
            "date": date,
            "strikePrice": strikePrice,
            "option": option,
            "LTP": LTP,
            "LTQ": LTQ,
            "totalTradedVolume": totalTradedVolume,
            "bestBid": bestBid,
            "bestAsk": bestAsk,
            "bestBidQty": bestBidQty,
            "bestAskQty": bestAskQty,
            "openInterest": openInterest,
            "changeInOi":changeInOi,
            "change": priceChange,
            # "IV": iv,
            "timestamp": timestamp,
            "sequence": sequence,
            "prevClosePrice": prevClosePrice,
            "prevOpenInterest": prevOpenInterest
        }

        # Store variables in MongoDB
        store_variables_in_mongodb(variables)

        # print(f"Symbol: {symbol}, Date: {date}, Strike Price: {strikePrice}, Option: {option}, LTP: {LTP}, LTQ: {LTQ}, Total Traded Volume: {totalTradedVolume}, Best Bid: {bestBid}, Best Ask: {bestAsk}, Best Bid Qty: {bestBidQty}, Best Ask Qty: {bestAskQty}, Open Interest: {openInterest}, Timestamp: {timestamp}, Sequence: {sequence}, Prev Close Price: {prevClosePrice}, Prev Open Interest: {prevOpenInterest}")

    # Introduce a delay of 5 seconds before processing the next line
    time.sleep(1)

# Wait for the command to finish (although it may not in this case)
process.wait()
