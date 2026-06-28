import streamlit as st
import json, os
import numpy as np
import matplotlib.pyplot as plt
from monte_carlo import simulate
np.random.seed(1)

#tracker data used if present, else demo defaults used
defaults = {"start_value": 25000, "contribution":50000}
config = json.load(open("config.json")) if os.path.exists("config.json") else defaults

st.title("£1M-by-35 projection")
st.caption("A Monte Carlo model of my own route to £1M")
growth = st.slider("Contribution growth (% per year)", 0.0, 5.0, 3.0, step=0.5) / 100
return_pct = st.slider("Annual real return (%)", 0.0, 10.0, 4.5, step=0.5) / 100
volatility = st.slider("Volatility (%)", 5.0, 25.0, 17.0, step=1.0) / 100


result = simulate(config["start_value"], config["contribution"],
                  return_pct, volatility, 11, contribution_growth=growth)
prob = (result>= 1_000_000).mean()

st.metric("Probability of £1M by age 35", f"{prob:.1%}")

fig, ax = plt.subplots()
ax.hist(result, bins=50)
p10 = np.percentile(result, 10)
ax.axvline(1000000, color="red", linestyle="--", label="£1M target")
ax.axvline(p10, color="orange", linestyle="--", label=f"10th percentile (£{p10:,.0f})")
ax.set_xlabel("Net worth at age 35 (£)")
ax.set_ylabel("number of simulations")
ax.set_title("Distribution of £1M outcomes")
ax.legend()
st.pyplot(fig)





