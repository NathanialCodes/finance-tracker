import numpy as np
import json
import os

defaults = {"start_value": 25000, "contribution": 50000}
if os.path.exists("config.json"):
    with open ("config.json") as f:
        config = json.load(f)
else:
    config = defaults

start_value = config["start_value"]
contribution = config["contribution"]

def simulate(start_value, contribution, mean_return, volatility, years, contribution_growth=0.0, n_sims=10000):
    
    pots = np.full(n_sims, start_value, dtype=float)
    current_contribution = contribution
    for year in range(years):
        returns = np.random.normal(mean_return, volatility, n_sims)
        pots = pots * (1 + returns) + current_contribution
        current_contribution = current_contribution * (1 + contribution_growth)
    return pots

if __name__ == "__main__": #This enables import into dashboard without printing function
    import json, os
    import matplotlib.pyplot as plt
    #config loading, the sweep and chart all indented now beneath this point

    scenarios = [
        ("Flat, 3%",    0.03, 0.0),
        ("Flat, 4.5%",    0.045, 0.0),
        ("Flat, 6%",    0.06, 0.0),
        ("Growing, 3%", 0.03, 0.03),
        ("Growing, 4.5%", 0.045, 0.03),
        ("Growing, 6%", 0.06, 0.03)
    ]   

    volatility = 0.17

    print(f"{'Scenario':<16}{'Age 35':>9}{'Age 36':>9}{'Age 37':>9}")

    for label, mean_return, contribution_growth in scenarios:
        probs = []
        for years in [11, 12, 13]:
                
            result = simulate(start_value, contribution, mean_return, volatility, years, contribution_growth)
                #print("min:", result.min(), "max:", result.max())
            probs.append((result >= 1000000).mean())

        print(f"{label:<16}{probs[0]:>9.1%}{probs[1]:>9.1%}{probs[2]:>9.1%}")

    import matplotlib.pyplot as plt

    result = simulate(start_value, contribution, 0.045, 0.17, 11, contribution_growth=0.03)

    plt.hist(result, bins=50)

    plt.axvline(1000000, color="red", linestyle="--", label="£1m target")
    p10 = np.percentile(result, 10)
    plt.axvline(p10, color="orange", linestyle="--", label=f"10th percentile (£{p10:,.0f})")

    plt.xlabel("Net worth at age 35 (£)")
    plt.ylabel("number of simulations")
    plt.title("Distribution of £1m outcomes - growing 4.5% case, age 35")
    plt.legend()
    plt.show()

