import yfinance as yf

def get_updated_stock_data(ticker_list: list[str] = ["PANW"], num_of_days: int = 14) -> None:

    stock_data = yf.download(
        tickers=" ".join(ticker_list),
        period=f"{num_of_days}d",
        interval="1d",
        group_by="ticker",
        auto_adjust=True
    )

    return stock_data

def get_closing_stock_data(ticker_list: list[str], stock_data: any) -> dict:
    map_of_stock_data = {}

    for ticker in ticker_list:
        closing_data = stock_data[ticker]['Close']
        map_of_stock_data[ticker] = closing_data

    return map_of_stock_data