import yfinance as yf

def get_prices():
    vuag = yf.Ticker("VUAG.L")
    vuag_price = vuag.history(period="5d")["Close"].dropna().iloc[-1]
    
    gdx = yf.Ticker("GDX")
    gdx_price_usd = gdx.history(period="5d")["Close"].dropna().iloc[-1]
    
    gu = yf.Ticker("GBPUSD=X")
    gbp_usd_rate = gu.history(period="5d")["Close"].dropna().iloc[-1] #GBP/USD exhange rate
    
    prices = {
        "VUAG.L": vuag_price,
        "GDX": gdx_price_usd / gbp_usd_rate,
    }
    return prices