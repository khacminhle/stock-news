import requests
from twilio.rest import Client

# Stock Market AI Set Up
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_ADVANTAGE_API_ENDPOINT = "https://www.alphavantage.co/query?"
ALPHA_API_KEY = "AALSPXS4HXM2RRYO"

# New Market API Set Up
NEWS_API_KEY = "c287afdaaeac467daa9a1d88c2715afb"
NEWS_URL = "https://newsapi.org/v2/everything"

# Twilio API Set Up
ACCOUNT_SID = "AC3389931e59d9a7be40f6f32a20062a44"
AUTH_TOKEN = "3f103e1cc2c656cbfb990a3dd465dcd0"
client = Client(ACCOUNT_SID, AUTH_TOKEN)




def calculate_5pct_movement():
    """This function calculate daily movement stock for 5% movement [True/False, percent change]"""
    pct_change = (latest_day_data_close - previous_day_data_close) / latest_day_data_close
    if pct_change > 0.00001:
        return True, pct_change
    elif pct_change < -0.00001:
        return True, pct_change
    else:
        return False

def sms_3_news():
    for item in top_3_news:
        title = item["title"]
        brief = item["description"]
        daily_movement = round(calculate_5pct_movement()[1] * 100, 2)

        if daily_movement > 0:
            direction = "🔺"
        else:
            direction = "🔻"

        message = client.messages \
            .create(
            body=f"{COMPANY_NAME}: {direction}{daily_movement}%\n"
                 f"Headline: {title}\n"
                 f"Brief: {brief}",
            from_='+19285850313',
            to='+61450306112'
        )

        print(message.status)


# def print_3_news():
#     for item in top


# # # STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol":STOCK,
    "apikey": ALPHA_API_KEY
}

news_params = {
    "apiKEY": NEWS_API_KEY,
    "q": COMPANY_NAME
}

stock_response = requests.get(url=ALPHA_ADVANTAGE_API_ENDPOINT, params=stock_params)
stock_response.raise_for_status()
# Pull stock market data
daily_data = list(stock_response.json()["Time Series (Daily)"].items())

latest_day_data_close = float(daily_data[0][1]["4. close"])
previous_day_data_close = float(daily_data[1][1]["4. close"])


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
# Pull new data
new_data = requests.get(url=NEWS_URL, params=news_params)
new_data.raise_for_status()
top_3_news = new_data.json()["articles"][:3]


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

if calculate_5pct_movement():
    print("Code ran")
    sms_3_news()


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

