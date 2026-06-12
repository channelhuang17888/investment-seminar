import json, datetime, os, time
import yfinance as yf

TSE = ['1612','2059','2303','2316','2327','2329','2330','2385','2454','3026','3324']
OTC = ['3042','3059','3167','3450','3485','3653','5289','5511','6121','6147','6223','6227','6442','6449','6669','6788','6840','7871','8299','9939']

os.makedirs('data', exist_ok=True)
prices = {}
updated = datetime.datetime.now(datetime.timezone.utc).isoformat()

def fetch(code, suffix):
    sym = code + suffix
    for attempt in range(3):
        try:
            t = yf.Ticker(sym)
            hist = t.history(period='2y', interval='1d', auto_adjust=True)
            if hist.empty:
                raise ValueError('empty')
            ohlc = []
            for dt, row in hist.iterrows():
                try:
                    d = dt.strftime('%Y-%m-%d')
                    o = round(float(row['Open']), 2)
                    h = round(float(row['High']), 2)
                    l = round(float(row['Low']), 2)
                    c = round(float(row['Close']), 2)
                    if o and h and l and c:
                        ohlc.append({'time':d,'open':o,'high':h,'low':l,'close':c})
                except:
                    pass
            with open('data/' + code + '.json', 'w') as f:
                json.dump({'updated': updated, 'data': ohlc}, f, separators=(',',':'))
            info = t.fast_info
            p = round(float(info.last_price or 0), 2)
            prev = round(float(info.previous_close or 0), 2)
            chg = round((p - prev) / prev * 100, 2) if prev > 0 else 0
            print('OK', sym, p, flush=True)
            return {'p': p, 'prev': prev, 'chgPct': chg}
        except Exception as e:
            print('RETRY', attempt+1, sym, e, flush=True)
            time.sleep(3)
    return None

for code in TSE:
    r = fetch(code, '.TW')
    if r:
        prices[code] = r
    time.sleep(0.5)

for code in OTC:
    r = fetch(code, '.TWO')
    if r:
        prices[code] = r
    time.sleep(0.5)

with open('data/prices.json', 'w') as f:
    json.dump({'updated': updated, 'prices': prices}, f, separators=(',',':'))

print('Done:', len(prices), '/', len(TSE)+len(OTC), flush=True)
