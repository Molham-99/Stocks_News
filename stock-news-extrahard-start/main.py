import requests
import smtplib
from twilio.rest import Client
MY_EMAIL = "*********@gmail.com"
PASSWORD = "*************"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_API = "https://www.alphavantage.co/query"
NEWS_API = "https://newsapi.org/v2/everything"
ALPHA_API_KEY = "ZSPFF5RNDRYAU3XF"
NEWS_API_KEY = "8959f3f6bfb94d6bb271be8349a98731"
m_account_sid = "YOUR ACCOUNT SID"
m_auth_token = "YOUR AUTH TOKEN"
close_list = []

parameters_alpha = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "interval": "60min",
    "apikey": ALPHA_API_KEY
}


def news(per):
    parameters_news = {
        "q": COMPANY_NAME,
        "from": yesterday,
        "sortBy": "relevancy",
        "language": "en",
        "apikey": NEWS_API_KEY
    }
    response = requests.get(NEWS_API, parameters_news)
    response.raise_for_status()
    news_data = response.json()
    title_1 = news_data["articles"][0]["title"]
    description_1 = news_data["articles"][0]["description"]
    url_1 = news_data["articles"][0]["url"]
    title_2 = news_data["articles"][1]["title"]
    description_2 = news_data["articles"][1]["description"]
    url_2 = news_data["articles"][1]["url"]
    title_3 = news_data["articles"][2]["title"]
    description_3 = news_data["articles"][2]["description"]
    url_3 = news_data["articles"][2]["url"]
    client = Client(m_account_sid, m_auth_token)
    mess = (f"Subject: STOCKS NEWS {per}\n\n1_The Title:\n {title_1}\n The Description :\n {description_1}\n"
            f" URL: {url_1}\n\n"
                     f"2_The Title:\n {title_2}\n The Description :\n {description_2}\n URL: {url_2}\n\n"
                     f"3_The Title:\n {title_3}\n The Description :\n {description_3}\n URL: {url_3}\n\n")
    message = client.messages.create(
        body=mess.encode(encoding="ascii", errors="ignore"),
        from_="+16075233375",
        to="+420773189554",
    )
    print(message.sid)
    #  IN CASE WE NEED TO SEND BY EMAIL
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="molham99m@gmail.com",
            msg=mess.encode(encoding="ascii", errors="ignore")
        )


response = requests.get(ALPHA_API, parameters_alpha)
response.raise_for_status()
alpha_data = response.json()
close = alpha_data["Time Series (Daily)"]
for day in close:
    close_list.append(day)
yesterday = close_list[0]
day_before_yesterday = close_list[1]
yesterday_close = float(close[yesterday]["4. close"])
day_before_yesterday_close = float(close[day_before_yesterday]["4. close"])
if yesterday_close > day_before_yesterday_close:
    different = yesterday_close - day_before_yesterday_close
    percentage = (different / day_before_yesterday_close) * 100
    if percentage >= 5:
        percent = round(percentage, 2)
        news(f"{percent}%")
else:
    different = day_before_yesterday_close - yesterday_close
    percentage = (different / yesterday_close) * 100
    if percentage >= 5:
        percent = round(percentage, 2)
        news(f"-{percent}%")
