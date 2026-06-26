import yfinance as yf

def fetch_latest(ticker):
    data = yf.Ticker(ticker).history(period="5d")
    return data["Close"].dropna().iloc[-1]

def get_prices():
    gbp_usd = fetch_latest("GBPUSD=X")
    return {
        "VUAG.L": fetch_latest("VUAG.L"),
        "GDX": fetch_latest("GDX") / gbp_usd,
        "GC=F": fetch_latest("GC=F") / gbp_usd, #gold, USD/oz -> GBP/oz
        "SI=F": fetch_latest("SI=F") / gbp_usd, #silver, USD/oz -> GBP/oz
    }
