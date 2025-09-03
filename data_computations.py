import pandas as pd
import numpy as np

def compute_ema(stock_value_data: any, ema_spans: list[int] = [8, 13, 21]) -> dict:
    df = pd.DataFrame(stock_value_data)
    map_of_ticker_emas = {}

    # compute ema for each span
    for ticker in df:
        # get dates
        if 'dates' not in map_of_ticker_emas.keys():
            map_of_ticker_emas['dates'] = list(df[ticker].index)
        # get ema values
        map_of_ticker_emas[ticker] = {}
        for span in ema_spans:
            map_of_ticker_emas[ticker][span] = list(df[ticker].ewm(span=span, adjust=False).mean())


    return map_of_ticker_emas