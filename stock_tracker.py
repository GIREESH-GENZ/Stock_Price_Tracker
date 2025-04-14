import yfinance as yf
import schedule
import time
import requests


MAILJET_API_KEY = 'aea2b62e3f2148306f5dbe31c8ca1caa'
MAILJET_SECRET_KEY = 'e289f79103074bdc572666a8e0e68a70'
SENDER_EMAIL = 'gireeshpolumuru@gmail.com'  

symbols = input("Enter the stock symbols separated by commas (e.g. AAPL,MSFT,GOOG): ").upper().split(",")
receiver_email = input("Enter the email address to receive stock alerts: ")

previous_prices = {}

def send_email(receiver_email, subject, message):
    url = "https://api.mailjet.com/v3.1/send"
    data = {
        'Messages': [{
            "From": {
                "Email": SENDER_EMAIL,
                "Name": "Stock Tracker"
            },
            "To": [{
                "Email": receiver_email,
                "Name": "User"
            }],
            "Subject": subject,
            "TextPart": message
        }]
    }

    response = requests.post(
        url,
        auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY),
        json=data
    )

    if response.status_code == 200:
        print(f"✅ Email sent to {receiver_email}")
    else:
        print(f"❌ Failed to send email. Response: {response.text}")

def fetch_stock_prices():
    for symbol in symbols:
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period="1d")
            current_price = round(data["Close"][-1], 2)
            print(f"{symbol} stock price is ₹{current_price}")

            # Send initial or changed price mail
            if symbol not in previous_prices:
                subject = f"{symbol} Current Price Alert"
                message = f"The current price of {symbol} is ₹{current_price}"
                send_email(receiver_email, subject, message)
                previous_prices[symbol] = current_price
            elif previous_prices[symbol] != current_price:
                subject = f"{symbol} Price Changed!"
                message = f"The price of {symbol} changed to ₹{current_price}"
                send_email(receiver_email, subject, message)
                previous_prices[symbol] = current_price

        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")

#  Instant email when script runs
fetch_stock_prices()

#  Schedule it every 5 minutes
schedule.every(5).minutes.do(fetch_stock_prices)

print("📈 Stock tracker is running...")
while True:
    schedule.run_pending()
    time.sleep(1)
