from datetime import datetime
from tinkoff.invest import Client, RequestError, OrderDirection, OrderType

import tinkoff_creds
from pandas import DataFrame


TOKEN = tinkoff_creds.test_token_v2


def buy(ticker):
    """
    Функция для покупки акции по ticker
    """
    try:
        with Client(TOKEN) as client:
            # Получаем figi по названию ticker
            figi = get_figi(ticker=ticker)

            request_to_buy = client.orders.post_order(
                order_id=str(datetime.utcnow().timestamp()),
                figi=figi,
                quantity=1,
                account_id=tinkoff_creds.account_id_test,
                direction=OrderDirection.ORDER_DIRECTION_BUY,
                order_type=OrderType.ORDER_TYPE_MARKET
            )

            print(request_to_buy)

    except RequestError as ex:
        return ex


def sell(ticker):
    """
    Функция для продажи акции по ticker
    """
    try:
        with Client(TOKEN) as client:
            # Получаем figi по названию ticker
            figi = get_figi(ticker=ticker)

            request_to_sell = client.orders.post_order(
                order_id=str(datetime.utcnow().timestamp()),
                figi=figi,
                quantity=1,
                account_id=tinkoff_creds.account_id_test,
                direction=OrderDirection.ORDER_DIRECTION_SELL,
                order_type=OrderType.ORDER_TYPE_MARKET
            )
            
            print(request_to_sell)

    except RequestError as ex:
        return ex


def get_figi(ticker):
    """
    Функция для получения figi по ticker
    """
    try:
        with Client(TOKEN) as client:
            instruments = client.instruments
            df = DataFrame(instruments.shares().instruments, columns=['name', 'figi', 'ticker'])

            instrument_figi = df[df['ticker'] == ticker]['figi'].iloc[0]
            instrument_name = df[df['ticker'] == ticker]['name'].iloc[0]

            return instrument_figi

    except RequestError as ex:
        return ex


def get_ticker(figi):
    """
    Функция для получения ticker по figi
    """
    try:
        with Client(TOKEN) as client:
            instruments = client.instruments
            df = DataFrame(instruments.shares().instruments, columns=['name', 'figi', 'ticker'])

            instrument_ticker = df[df['figi'] == figi]['ticker'].iloc[0]

            return instrument_ticker

    except RequestError as ex:
        return ex


def get_current_stocks():
    """
    Функция для получения акций в портфеле
    """
    try:
        with Client(TOKEN) as client:
            instruments = client.operations.get_positions(account_id=tinkoff_creds.account_id_test)

            df = DataFrame(instruments.securities, columns=['figi', 'balance'])

            stocks = list(df['figi'])

            return stocks
            # print('BBG00F9XX7H4' in stocks)
            # print(instruments)

    except RequestError as ex:
        return ex


# def main():
#     try:
#         with Client(TOKEN) as client:
#             print(client.users.get_accounts())
#     except RequestError as ex:
#         print(str(ex))


# if __name__ == "__main__":
#     pass
    # main()
    # buy(ticker='RNFT')
    # sell(ticker='RNFT')
    # print(get_ticker('BBG00F9XX7H4'))
    # get_current_stocks_value()
    # with Client(TOKEN) as client:
        
    #     print(client.users.get_accounts())
        # instruments = client.instruments
        # instruments_df = DataFrame(instruments.shares().instruments, columns=['name', 'figi', 'ticker'])
        # instrument_figi = instruments_df[instruments_df['ticker'] == 'RNFT']

        # print(instrument_figi)
        # positions = client.operations.get_portfolio(account_id=tinkoff_creds.account_id_test).positions
        # print(positions[0])

        # raw_pos = client.operations.get_positions(account_id=tinkoff_creds.account_id_test)
