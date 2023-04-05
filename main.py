import requests
import datetime as dt
from twilio.rest import Client

account_sid = "AC3a42f84005a94f1eadfd79b8b94be92e"
auth_token = "66cc32bcb612798a8f854a67121996ac"

NEWS_API_KEY = "6e96514db24b4bf99c7e07de2ef7a21b"
NEWS_API = "https://newsapi.org/v2/everything"
NEWS_PARAMS = {
    'q': 'tesla',
    'sources': 'CNN',
    'apiKey': NEWS_API_KEY
}

STOCK = "TSLA"
ALPHA_ADVANTAGE_API_KEY = "54GD66CWFWW8OWK2"
ALPHA_ADVANTAGE_API = "https://www.alphavantage.co/query"
ALPHA_ADVANTAGE_PARAMS = {
    'function': 'TIME_SERIES_DAILY_ADJUSTED',
    'symbol': STOCK,
    'apikey': ALPHA_ADVANTAGE_API_KEY
}
yesterday = dt.date.today() - dt.timedelta(days=1)
day_before_yesterday = dt.date.today() - dt.timedelta(days=2)

stock_price = requests.get(ALPHA_ADVANTAGE_API, params=ALPHA_ADVANTAGE_PARAMS)
stock_price.raise_for_status()

data = stock_price.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]

yesterday_data = float(data_list[0]['4. close'])
day_before_yesterday_data = float(data_list[1]['1. open'])

symbol = ""

difference = yesterday_data * 100 / day_before_yesterday_data - 100.00

if difference > 0:
    symbol = "🔺"
else:
    symbol = "🔻"

if difference >= 5 or difference <= -5:
    news_response = requests.get(NEWS_API, params=NEWS_PARAMS)
    news_response.raise_for_status()
    news = news_response.json()['articles'][0]
    news_title = news['title']
    news_brief = news['description']

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=f'TSLA: {symbol}{abs(difference)}%\nHeadline: {news_title}\n\nBrief: {news_brief}',
        to='whatsapp:+918279576916'
    )
