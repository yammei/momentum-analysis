Generates user-readable insights from OHLC data.

Analysis Logic
1. A cluster of exponential moving averages (EMAs) at spans 8-13-21 are computed for momentum comparisons.
2. The configuration and degree of spread from EMA cluster indicates potential momentum.
3. The alignment and distance of Open-High-Low-Close (OHLC) against EMA cluster validates trend assumptions.

Service Architecture
Dev site auto-request <-> FastAPI CRUD in K8s pod <-> Daily-updated Postgres DB <-> Python data workflow

```bash
python3 main.py

[0] Retrieving stock data.
[*********************100%***********************]  11 of 11 completed
[1] Extracting closing values.
[2] Computing EMA values.
[3] Visualizing all data.
[4] Analyzing stock data.

['PANW']
['ema_spread_score']: 1.22%
['distance']: 2.07%
['above_share']: 0.00%
['inside_share']: 34.01%
['below_share']: 65.99%

['NVDA']
['ema_spread_score']: -0.10%
['distance']: -0.37%
['above_share']: 22.06%
['inside_share']: 74.25%
['below_share']: 3.69%

...

[5] Translating metrics.

['PANW']
['ema_analysis']: Upward velocity of 1.22%.
['distance_analysis']: Prices trading above short-term trends by 2.07%.
['share_analysis']: Buyer dominance. Trend base below prices (65.99% of EMA band above prices).

['NVDA']
['ema_analysis']: Mild downward velocity of 0.10%.
['distance_analysis']: Prices trading below short-term trends by 0.37%.
['share_analysis']: Market indecision. Trend base in line with prices (22.06% overlap).

...

```
PANW Graph EMA8-13-21 + OHLC Overlay | 09.02.2025
![PANW graph](https://github.com/yammei/momentum-analysis/blob/main/graphs/PANW_EMA8-13-21_overlaid.png)

NVDA Graph EMA8-13-21 + OHLC Overlay | 09.02.2025
![NVDA graph](https://github.com/yammei/momentum-analysis/blob/main/graphs/NVDA_EMA8-13-21_overlaid.png)