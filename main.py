# custom libraries
from stock_retriever import get_updated_stock_data, get_closing_stock_data
from data_computations import compute_ema
from data_visualizations import graph_ema
from data_analysis import compute_trends
from user_readables import translate_metrics

def main():
    # list of top tech companies
    ticker_list = [
        'PANW',
        'NVDA',
        'MSFT',
        'AAPL',
        'AMZN',
        'GOOG',
        'META',
        'AVGO',
        'CRM',
        'ORCL',
        'CSCO'
    ]
    span_list = [8, 13, 21]

    # get updated stock data
    print(f"[0] Retrieving stock data.")
    updated_stock_data = get_updated_stock_data(
        ticker_list = ticker_list,
        num_of_days = span_list[-1]
    )
    # print(f"updated_stock_data: {updated_stock_data}")

    # get closing data for each ticker
    print(f"[1] Extracting closing values.")
    closing_stock_data = get_closing_stock_data(
        ticker_list = ticker_list,
        stock_data = updated_stock_data
    )

    # compute sets of ema values for each ticker
    print(f"[2] Computing EMA values.")
    computed_ema_values = compute_ema(
        stock_value_data = closing_stock_data,
        ema_spans = span_list
    )

    # visualize all data
    print(f"[3] Visualizing all data.")
    graph_ema(
        ema_data = computed_ema_values,
        display = False,
        save = True,
        overlay_og_data = updated_stock_data
    )

    print(f"[4] Analyzing stock data.")
    metrics = compute_trends(
        og_stock_data = updated_stock_data,
        ema_data = computed_ema_values,
        print_results = True
    )

    print(f"[5] Translating metrics.")
    translate_metrics(
        metrics = metrics
    )

if __name__ == '__main__':
    main()