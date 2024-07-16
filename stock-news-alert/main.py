import requests
import os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

TWILIO_SID = "YOUR SID"
TWILIO_AUTH_TOKEN = "yOUR AUTH_TOKEN"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
api_key = os.environ.get("stocks_api_key")
language = "en"
sortBy = "popularity"
news_api_key = "YOUR API KEY"


"""This section does the work of getting the closing price of stock"""
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK_NAME}&apikey={api_key}'
r = requests.get(url)
data = r.json()


yesterday_date = '2024-03-13'
yesterdays_closing_price = float([value['4. close'] for key, value in data['Time Series (Daily)'].items() if key ==
                                  yesterday_date][0])


day_before_yesterday = '2024-03-12'
day_before_yesterday_closing_price = float([value['4. close'] for key, value in data['Time Series (Daily)'].items()
                                            if key == day_before_yesterday][0])

"""Difference between yesterdays adn day before yesterdays stock is calculated"""
diff_between_stocks = yesterdays_closing_price - day_before_yesterday_closing_price
up_down = None
if diff_between_stocks > 0:
    up_down = "🔺"
else:
    up_down = "🔻"


average = (yesterdays_closing_price + day_before_yesterday_closing_price) / 2
percentage_difference = abs(round((diff_between_stocks / average) * 100))


"""Read the documentation thoroughly and see which parameters are the most required """
"""The news related to the stock is fetched if there is fluctuation"""
if abs(percentage_difference) >= 5:
    parameters = {
        "qInTitle": COMPANY_NAME,
        "apiKey": news_api_key,
        "language": language
    }

    r = requests.get(NEWS_ENDPOINT, params=parameters)
    data = r.json()["articles"]

    list_of_Articles = data[:3]

    """The section does the work of sending an sms with help of twilio"""
    formatted_articles_list = [f" {STOCK_NAME}: {up_down}{percentage_difference}%\n  " 
                               f"Headline: {article['title']}. \nBrief: {article['description']}." for article
                               in list_of_Articles]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles_list:
        message = client.messages.create(
            body=article,
            from_="+15715703630",
            to="+918433643741"
        )
