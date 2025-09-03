import numpy as np
import json
import os

def compute_trends(og_stock_data: 'df' = None, ema_data: 'df' = None, print_results: bool = False) -> dict:
    if og_stock_data is None or ema_data is None:
        print(f"type(og_stock_data): {type(og_stock_data)} | type(ema_data): {type(ema_data)}")
        return

    metrics = {}

    for k1 in ema_data.keys():
        ema_spans = sorted(ema_data[k1].keys(), key=int)
        most_recent_trend = 0
        metrics[k1] = {
            'ema_spread_score': 0,
            'distance': 0,
            'above_share':  0,
            'inside_share': 0,
            'below_share':  0
        }
        n = len(ema_data[k1][ema_spans[0]])
        for i in range(n - 1, -1, -1):                
            ema_values = [ema_data[k1][ema_span][i] for ema_span in ema_spans]
            candle_values = {
                'open': og_stock_data[k1]['Open'].iloc[i],
                'close': og_stock_data[k1]['Close'].iloc[i],
                'high': og_stock_data[k1]['High'].iloc[i],
                'low': og_stock_data[k1]['Low'].iloc[i]
            }
            center_approx = (og_stock_data[k1]['High'].iloc[i] - og_stock_data[k1]['Low'].iloc[i]) / 2

            # compute spread score
            curr_spread_score  = ema_values[1] - ema_values[0]
            curr_spread_score += ema_values[2] - ema_values[1]
            curr_spread_score /= candle_values['close'] * -1
            metrics[k1]['ema_spread_score'] += curr_spread_score

            # compute candle-cluster distance
            curr_distance = (candle_values['close'] - np.mean(ema_values)) / candle_values['close']
            metrics[k1]['distance'] += curr_distance

            # compute share
            if i == 0:
                metrics[k1]['inside_share'] += 1.0
                continue
            else:
                sorted_ema_values = sorted(ema_values)
                range_of_candle = max(1e-9, (candle_values['high'] - candle_values['low']))
                range_of_spread = max(1e-9, (sorted_ema_values[-1] - sorted_ema_values[0]))

                curr_above_share  = max(candle_values['high'], sorted_ema_values[-1])
                curr_above_share -= max(candle_values['high'], sorted_ema_values[0])
                metrics[k1]['above_share'] += curr_above_share / range_of_spread

                curr_inside_share  = min(candle_values['high'], max(candle_values['low'], sorted_ema_values[-1]))
                curr_inside_share -= max(candle_values['low'], min(candle_values['high'], sorted_ema_values[0]))
                metrics[k1]['inside_share'] += curr_inside_share / range_of_spread

                curr_below_share  = min(candle_values['low'], sorted_ema_values[-1])
                curr_below_share -= min(candle_values['low'], sorted_ema_values[0])
                metrics[k1]['below_share'] += curr_below_share / range_of_spread

        # compute means
        metrics[k1]['ema_spread_score'] /= n
        metrics[k1]['distance']         /= n
        metrics[k1]['above_share']      /= n
        metrics[k1]['inside_share']     /= n
        metrics[k1]['below_share']      /= n

    if print_results:
        for k, v in metrics.items():
            print(f"['{k}']")
            print(f"['ema_spread_score']: {(metrics[k]['ema_spread_score'] * 100):.2f}%")
            print(f"['distance']: {(metrics[k]['distance'] * 100):.2f}%")
            print(f"['above_share']: {(metrics[k]['above_share'] * 100):.2f}%")
            print(f"['inside_share']: {(metrics[k]['inside_share'] * 100):.2f}%")
            print(f"['below_share']: {(metrics[k]['below_share'] * 100):.2f}%")
            print()

    return metrics
