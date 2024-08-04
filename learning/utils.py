# import requests

# def get_stock_price(symbol):
#     API_KEY = 'your_alpha_vantage_api_key'
#     url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={API_KEY}'
#     response = requests.get(url)
#     data = response.json()
#     if 'Time Series (1min)' in data:
#         latest_time = sorted(data['Time Series (1min)'].keys())[0]
#         return data['Time Series (1min)'][latest_time]['1. open']
#     return None
