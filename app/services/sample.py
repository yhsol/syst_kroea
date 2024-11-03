import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import yaml
from app.core.utils import KoreaInvestAPI, KoreaInvestEnv

ORD_DVSN = {
    "지정가": "00",
    "시장가": "01",
    "조건부지정가": "02",
    "최유리지정가": "03",
    "최우선지정가": "04",
    "장전 시간외": "05",
    "장후 시간외": "06",
    "시간외 단일가": "07",
    "자기주식": "08",
    "자기주식S-Option": "09",
    "자기주식금전신탁": "10",
    "IOC지정가": "11",
    "FOK지정가": "12",
    "IOC시장가": "13",
    "FOK시장가": "14",
    "IOC최유리": "15",
    "FOK최유리": "16",
}


def main():
    with open(r'config.yaml', encoding='UTF-8') as f:
        _cfg = yaml.load(f, Loader=yaml.FullLoader)
        env_cls = KoreaInvestEnv(_cfg)
        base_headers = env_cls.get_base_headers()
        cfg = env_cls.get_full_config()
        korea_invest_api = KoreaInvestAPI(cfg, base_headers)
        
        # 주식현재가 조회 TR
        stock_code = "005930"
        price_info_map = korea_invest_api.get_current_price(stock_code)
        # print("price_info_map: ", price_info_map)

        # 주식현재가 호가/예상 체결 TR
        stock_code = "005930"
        hoga_info = korea_invest_api.get_hoga_info(stock_code)
        # print("hoga_info: ", hoga_info)

        # 주식 잔고 조회 TR
        stock_code = "005930"
        account_balance, details_df = korea_invest_api.get_account_balance(stock_code)
        # print(f"account_balance: {account_balance:,}원")
        # print("details_df: ", details_df)

        # 전일대비 등락률 순위 (부호 절댓값 적용)
        rank_info = korea_invest_api.get_fluctuation_rank()
        print("rank_info: ", rank_info)

        # # 삼성전자 8만원에 1주 지정가 매수 주문
        # stock_code = "005930"
        # price = 80000
        # quantity = 1
        # order_result = korea_invest_api.do_buy_order(stock_code, order_qty=quantity, order_price=price, order_type=ORD_DVSN["지정가"])
        # order_no = order_result.get_body().output["ODNO"]
        # print("order_result: ", order_result)

        # # 주문 취소
        # order_cancel_result = korea_invest_api.do_cancel_order(order_no, order_qty=quantity)
        # print("order_cancel_result: ", order_cancel_result)

        # # 주문 정정
        # order_revise_result = korea_invest_api.do_revise_order(order_no, order_qty=quantity, order_price=price)
        # print("order_revise_result: ", order_revise_result)

        # # 미체결 주문 조회
        # order_unexecuted_result = korea_invest_api.get_orders()
        # print("order_unexecuted_result: ", order_unexecuted_result)

        # # 삼성전자 시장가 매수 주문
        # stock_code = "005930"
        # price = 0
        # quantity = 1
        # order_result = korea_invest_api.do_buy_order(stock_code, order_qty=quantity, order_price=price, order_type=ORD_DVSN["시장가"])
        # print("order_result: ", order_result)

        # # 삼성전자 7만원에 1주 지정가 매도 주문
        # stock_code = "005930"
        # price = 70000
        # quantity = 1
        # order_result = korea_invest_api.do_sell_order(stock_code, order_qty=quantity, order_price=price, order_type=ORD_DVSN["지정가"])
        # print("order_result: ", order_result)

        # # 삼성전자 시장가 매도 주문
        # stock_code = "005930"
        # price = 0
        # quantity = 1
        # order_result = korea_invest_api.do_sell_order(stock_code, order_qty=quantity, order_price=price, order_type=ORD_DVSN["시장가"])
        # print("order_result: ", order_result)

        # 해외주식

        # 주식현재가 시세 TR
        exchange_code = "NAS"
        stock_code = "AAPL"
        price_info_map = korea_invest_api.get_current_price_overseas(exchange_code, stock_code)
        print("price_info_map: ", price_info_map)

        # 해외주식 잔고
        account_balance, details_df = korea_invest_api.get_account_balance_overseas()
        print("account_balance: ", account_balance)
        print("details_df: ", details_df)

        # 해외주식 지정가 매수 주문
        exchange_code = "NASD"
        stock_code = "AAPL"
        order_type = ORD_DVSN["지정가"]
        price = 150
        quantity = 1
        order_result = korea_invest_api.do_buy_order_overseas(exchange_code, stock_code, order_type, price, quantity)
        print("order_result: ", order_result)

        # 해외주식 시장가 매수 주문 
        # => 시장가 주문이 공식적으로 지원은 안되는 듯.
        # 일단 지정가 타입으로 하고, price 를 0 으로 해서 테스트.
        # 위의 방법으로 안돼면 호가정보를 조회해서 최유리 호가를 사용하는 방법을 시도해봐야 함.
        exchange_code = "NASD"
        stock_code = "AAPL"
        order_type = ORD_DVSN["시장가"]
        price = 0
        quantity = 1
        order_result = korea_invest_api.do_buy_order_overseas(exchange_code, stock_code, order_type, price, quantity)
        print("order_result: ", order_result)

        # 해외주식 지정가 매도 주문
        exchange_code = "NASD"
        stock_code = "AAPL"
        order_type = ORD_DVSN["지정가"]
        price = 150
        quantity = 1
        order_result = korea_invest_api.do_sell_order_overseas(exchange_code, stock_code, price, quantity, order_type)
        print("order_result: ", order_result)

        # 해외주식 시장가 매도 주문
        exchange_code = "NASD"
        stock_code = "AAPL"
        order_type = ORD_DVSN["시장가"]
        price = 0
        quantity = 1
        order_result = korea_invest_api.do_sell_order_overseas(exchange_code, stock_code, price, quantity, order_type)
        print("order_result: ", order_result)

if __name__ == "__main__":
    main()