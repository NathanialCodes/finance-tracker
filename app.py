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
st.write(
    "This model runs 10,000 simulated market paths from my projected 2029 "
    "starting pot, saving a fixed amount each year, to estimate my probability "
    "of reaching £1M net worth. Drag the sliders to change the assumptions."
)

growth = st.slider("Contribution growth (% per year)", 0.0, 5.0, 3.0, step=0.5) / 100
return_pct = st.slider("Annual real return (%)", 0.0, 10.0, 4.5, step=0.5) / 100
volatility = st.slider("Volatility (%)", 5.0, 25.0, 17.0, step=1.0) / 100


result_35 = simulate(config["start_value"], config["contribution"],
                  return_pct, volatility, 11, contribution_growth=growth)
result_36 = simulate(config["start_value"], config["contribution"],
                  return_pct, volatility, 12, contribution_growth=growth)
result_37 = simulate(config["start_value"], config["contribution"],
                  return_pct, volatility, 13, contribution_growth=growth)

st.subheader("Probability of reaching £1M")
col1, col2, col3 = st.columns(3)
col1.metric("By age 35", f"{(result_35 >= 1000000).mean():.1%}")
col2.metric("By age 36", f"{(result_36 >= 1000000).mean():.1%}")
col3.metric("By age 37", f"{(result_37 >= 1000000).mean():.1%}")


fig, ax = plt.subplots()
ax.hist(result_35, bins=50)
p10 = np.percentile(result_35, 10)
ax.axvline(1000000, color="red", linestyle="--", label="£1M target")
ax.axvline(p10, color="orange", linestyle="--", label=f"10th percentile (£{p10:,.0f})")
ax.set_xlabel("Net worth at age 35 (£)")
ax.set_ylabel("Number of simulations")
ax.set_title("Distribution of outcomes at age 35")
ax.legend()
st.pyplot(fig)





