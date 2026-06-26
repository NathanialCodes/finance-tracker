from prices import get_prices
from holdings import load_holdings

prices = get_prices()
df = load_holdings()

df["price"] = df["ticker"].map(prices)
df["live_value"] = df["units"] * df ["price"]
df["live_value"] = df["live_value"].fillna(df["value"]) #fills in the NaN values with the orginal value column

alloc = df.groupby("class")["live_value"].sum()
print((alloc / alloc.sum() * 100).round(1))
print(df["live_value"].sum().round(2)) # total live networth
