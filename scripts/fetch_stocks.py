import json, datetime, os, time
import yfinance as yf

STOCKS = {
    'tse': ['1612','2059','2303','2316','2327','2329','2330','2385','2454','3026','3324'],
    'otc': ['3042','3059','3167','3450','3485','3653','5289','5511','6121','6147','6223','6227','6442','6449','6669','6788','6840','7871','8299','9939']
}

os.makedirs('data', exist_ok=True)
prices = {}
updated = datetime.datetime.now(datetime.timezone.utc).isoformat()

for ex, codes in STOCKS.items():
    suffix = '.TW' if ex == 'tse' else '.TWO'
    for code in codes:
        ticker_sym = f'{code}{suffix}'
        for attempt in range(3):
            try:
                t = yf.Ticker(ticker_sym)
                hist = t.history(period='2y', interval='1d', auto_adjust=True)
                if hist.empty:
                    raise ValueError('empty dataframe')

                ohlc = []
                for dt, row in hist.iterrows():
                    try:
                        date_str = dt.strftime('%Y-%m-%d')
                        o = float(row['Open'])
                        h = float(row['High'])
                        l = float(row['Low'])
                        c = float(row['Close'])
                        if o and h and l and c:
                            ohlc.append({'time
