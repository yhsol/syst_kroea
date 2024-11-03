from collections import namedtuple
import copy
import json
import time
import pandas as pd
import requests
import logging

logger = logging.getLogger(__name__)

class KoreaInvestEnv:
    def __init__(self, cfg):
        self.cfg = cfg
        self.custtype = cfg['custtype']
        self.base_headers = {
            "Content-Type": "application/json",
            "Accept": "text/plain",
            "charset": "UTF-8",
            'User-Agent': cfg['my_agent'] 
        }

        self.using_url = cfg['url']
        self.api_key = cfg['api_key']
        self.api_secret_key = cfg['api_secret_key']
        self.stock_account_number = cfg['stock_account_number']
        self.websocket_approval_key = self.get_websocket_approval_key()
        self.account_access_token = self.get_account_access_token()
        self.base_headers["authorization"] = self.account_access_token
        self.base_headers["appkey"] = self.api_key
        self.base_headers["appsecret"] = self.api_secret_key
        self.cfg['websocket_approval_key'] = self.websocket_approval_key
        self.cfg['account_num'] = self.stock_account_number
        self.cfg['using_url'] = self.using_url

    def get_base_headers(self):
        return copy.deepcopy(self.base_headers)
    
    def get_full_config(self):
        return copy.deepcopy(self.cfg)

    def get_websocket_approval_key(self):
        headers = { "content-type": "application/json" }
        body = {
            "grant_type": "client_credentials",
            "appkey": self.api_key,
            "secretkey": self.api_secret_key
        }
        url = f"{self.using_url}/oauth2/Approval"
        res = requests.post(url, headers=headers, data=json.dumps(body))
        approval_key = res.json()['approval_key']
        return approval_key
    
    def get_account_access_token(self):
        p = {
            "grant_type": "client_credentials",
            "appkey": self.api_key,
            "appsecret": self.api_secret_key
        }
        url = f"{self.using_url}/oauth2/tokenP"
        res = requests.post(url, headers=self.base_headers, data=json.dumps(p))
        res.raise_for_status()
        my_token = res.json()['access_token']
        return f"Bearer {my_token}"

    def get_api_key(self):
        return self.cfg['api_key']

    def get_api_secret_key(self):
        return self.cfg['api_secret_key']
class KoreaInvestAPI:
    def __init__(self, cfg, base_headers):
        self.base_headers = base_headers
        self.custtype = cfg['custtype']
        self.websocket_approval_key = cfg['websocket_approval_key']
        self.account_num = cfg['account_num']
        self.stock_account_product_code = cfg['stock_account_product_code']
        self.hts_id = cfg['hts_id']
        self.using_url = cfg['using_url']

    def set_order_hash_key(self, headers, params):
        url = f"{self.using_url}/uapi/hashkey"

        res = requests.post(url, headers=headers, data=json.dumps(params))
        rescode = res.status_code
        if rescode == 200:
            headers['hashkey'] = res.json()['HASH']
        else:
            logger.error(f"Error in set_order_hash_key: {rescode}")
            return None

    def _url_fetch(self, url, tr_id, params, is_post=False, use_hash=False):
        try:
            url = f"{self.using_url}{url}"
            headers = self.base_headers
            headers["tr_id"] = tr_id
            headers["custtype"] = self.custtype

            if is_post:
                if use_hash:
                    self.set_order_hash_key(headers, params)
                res = requests.post(url, headers=headers, data=json.dumps(params))
            else:
                res = requests.get(url, headers=headers, params=params)

            if res.status_code != 200:
                logger.error(f"API request failed: {res.status_code}, {res.text}")
                return None
            else:
                ar = APIResponse(res)
                return ar
        except Exception as e:
            logger.error(f"API request failed: {e}")
            return None
        

    def get_account_info(self):
        url = f"{self.cfg['using_url']}/uapi/account/GetAccountInfo"
        res = requests.post(url, headers=self.base_headers)
        return res.json()
    
    def get_current_price(self, stock_code):
        url = "/uapi/domestic-stock/v1/quotations/inquire-price"
        tr_id = "FHKST01010100"
        
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": stock_code,
        }
        
        res = self._url_fetch(url, tr_id, params)
        
        if res is not None and res.is_ok():
            return res.get_body().output
        elif res is None:
            return dict()
        else:
            res.print_error()
            return dict()
    
    def get_hoga_info(self, stock_code):
        url = "/uapi/domestic-stock/v1/quotations/inquire-asking-price-exp-ccn"
        tr_id = "FHKST01010200"
        
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": stock_code,
        }
        
        res = self._url_fetch(url, tr_id, params)
        
        if res is not None and res.is_ok():
            return res.get_body().output1
        elif res is None:
            return dict()
        else:
            res.print_error()
            return dict()
    
    def get_account_balance(self, stock_code):
        url = "/uapi/domestic-stock/v1/trading/inquire-balance"
        tr_id = "TTTC8434R"
        
        params = {
            "CANO": self.account_num,
            "ACNT_PRDT_CD": self.stock_account_product_code,
            "AFHR_FLPR_YN": "N",
            "OFL_YN": "",
            "INQR_DVSN": "01",
            "UNPR_DVSN": "01",
            "FUND_STTL_ICLD_YN": "N",
            "FNCG_AMT_AUTO_RDPT_YN": "N",
            "PRCS_DVSN": "01",
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": "",
        }

        res = self._url_fetch(url, tr_id, params)
        output_columns = ["종목코드", "종목명", "보유수량", "주문가능수량", "매도가능수량", "매입단가", "수익률", "현재가", "전일대비증감", "전일대비 등락률", "총평가금액", "평가손익합계금액"]

        if res is None:
            return 0, pd.DataFrame(columns=output_columns)
        
        try:
            output1 = res.get_body().output1
        except Exception as e:
            logger.error(f"Error in get_account_balance: {e}")
            return 0, pd.DataFrame(columns=output_columns)
        
        if res is not None and res.is_ok() and output1:
            df = pd.DataFrame(output1)
            target_columns = ["pdno", "prdt_name", "hldg_qty", "ord_psbl_qty", "slpsb_qty", "pchs_unpr", "pftrt", "prpr", "bfdy_cprs_icdc", "fltt_rt", "tot_evlu_amt", "evlu_pfls_smtl_amt"]
            df = df[target_columns]
            df[target_columns[2:]] = df[target_columns[2:]].apply(pd.to_numeric, errors='coerce') # 종목 코드, 종목명 제외하고 형변환
            column_name_map = dict(zip(target_columns, output_columns))
            df.rename(columns=column_name_map, inplace=True)
            print("df1: ", df)
            df = df[df['보유수량'] != 0]
            print("df2: ", df)
            r2 = res.get_body().output2
            print("r2: ", r2)
            return int(r2[0]['tot_evlu_amt']), df
        else:
            print("res is not None and res.is_ok() and output1 is None or Empty")
            logger.info(f"Error in get_account_balance: {res.get_error_code()}")
            tot_evlu_amt = 0
            if res.is_ok():
                r2 = res.get_body().output2
                tot_evlu_amt = int(r2[0]['tot_evlu_amt'])
            return tot_evlu_amt, pd.DataFrame(columns=output_columns)
    
    def get_fluctuation_rank(self):
        url = "/uapi/domestic-stock/v1/ranking/fluctuation"
        tr_id = "FHPST01700000"
        
        params = {
            "fid_rsfl_rate2": "100",    
            "fid_cond_mrkt_div_code": "J",
            "fid_cond_scr_div_code": "20170",
            "fid_input_iscd": "0000",
            "fid_rank_sort_cls_code": "0",
            "fid_input_cnt_1": "0",
            "fid_prc_cls_code": "0",
            "fid_rank_sort_cls_code": "0",
            "fid_input_price_1": "",
            "fid_input_price_2": "",
            "fid_vol_cnt": "",
            "fid_trgt_cls_code": "0",
            "fid_trgt_exls_cls_code": "0",
            "fid_div_cls_code": "0",
            "fid_rsfl_rate1": "",
        }
        
        res = self._url_fetch(url, tr_id, params)

        if res is not None and res.is_ok():
            df = pd.DataFrame(res.get_body().output)
            target_columns = ["stck_shrn_iscd", "hts_kor_isnm", "prdy_ctrt", "cnnt_ascn_dynu", "hgpr_vrss_prpr_rate"]
            output_columns = ["주식 단축 종목코드", "HTS 한글 종목명", "전일 대비율", "연속 상승 일수", "최고가 대비 현재가 비율"]
            df = df[target_columns]
            # df[target_columns[1:]] = df[target_columns[1:]].apply(pd.to_numeric, errors='coerce')
            column_rename_map = dict(zip(target_columns, output_columns))
            df.rename(columns=column_rename_map, inplace=True)
            return df
        elif res is None:
            return dict()
        else:
            res.print_error()
            return dict()
        
    def do_order(self, stock_code, order_qty=1, order_price=0, is_buy=True, order_type="01", prd_code="01"):
        url = '/uapi/domestic-stock/v1/trading/order-cash'

        if is_buy:
            tr_id = "TTTC0802U" # 매수 주문
        else:
            tr_id = "TTTC0801U" # 매도 주문

        params = {
            "CANO": self.account_num,
            "ACNT_PRDT_CD": self.stock_account_product_code,
            "PDNO": stock_code,
            "ORD_DVSN": order_type,
            "ORD_QTY": str(order_qty),
            "ORD_UNPR": str(order_price),
            "CTAC_TLNO": "",
            "SLL_TYPE": "01",
            "ALGO_NO": "",
        }

        t1 = self._url_fetch(url, tr_id, params, is_post=True, use_hash=True)

        if t1 is not None and t1.is_ok():
            return t1
        elif t1 is None:
            return None
        else:
            t1.print_error()
            return None
    
    def do_sell_order(self, stock_code, order_qty, order_price, order_type):
        t1 = self.do_order(stock_code, order_qty, order_price, is_buy=False, order_type=order_type)
        return t1
    
    def do_buy_order(self, stock_code, order_qty, order_price, order_type):
        t1 = self.do_order(stock_code, order_qty, order_price, is_buy=True, order_type=order_type)
        return t1
    
    def _do_cancel_revise(self, order_no, order_qty, order_price, order_branch, prd_code, order_dv, cncl_dv, qty_all_yn):
        url = "/uapi/domestic-stock/v1/trading/order-rvsecncl"
        tr_id = "TTTC0803U"

        params = {
            "CANO": self.account_num,
            "ACNT_PRDT_CD": self.stock_account_product_code,
            "KRX_FWDG_ORD_ORGNO": order_branch,
            "ORGN_ODNO": order_no,
            "ORD_DVSN": order_dv,
            "RVSE_CNCL_DVSN_CD": cncl_dv,
            "ORD_QTY": str(order_qty),
            "ORD_UNPR": str(order_price),
            "QTY_ALL_ORD_YN": qty_all_yn,
        }

        t1 = self._url_fetch(url, tr_id, params, is_post=True)

        if t1 is not None and t1.is_ok():
            return t1
        elif t1 is None:
            return None
        else:
            t1.print_error()
            return None

    def do_cancel_order(self, order_no, order_qty, order_price="01", order_branch="06010", prd_code="01", order_dv="00", cncl_dv="02", qty_all_yn="Y"):
        return self._do_cancel_revise(order_no, order_qty, order_price, order_branch, prd_code, order_dv, cncl_dv, qty_all_yn)
    
    def do_revise_order(self, order_no, order_qty, order_price, order_branch="06010", prd_code="01", order_dv="00", cncl_dv="02", qty_all_yn="Y"):
        return self._do_cancel_revise(order_no, order_qty, order_price, order_branch, prd_code, order_dv, cncl_dv, qty_all_yn)
    
    def get_orders(self):
        url = "/uapi/domestic-stock/v1/trading/inquire-psbl-rvsecncl"
        tr_id = "TTTC8036R"

        params = {
            "CANO": self.account_num,
            "ACNT_PRDT_CD": self.stock_account_product_code,
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": "",
            "INQR_DVSN_1": "0", # 조회순서 0: 조회순, 1: 주문순, 2: 종목순
            "INQR_DVSN_2": "0", # 전체 0: 전체, 1: 매도, 2: 매수
        }

        t1 = self._url_fetch(url, tr_id, params)

        if t1 is not None and t1.is_ok() and t1.get_body().output:
            tdf = pd.DataFrame(t1.get_body().output)
            tdf.set_index("odno", inplace=True)
            cf1 = ['pdno', 'ord_qty', 'ord_unpr', 'ord_tmd', 'ord_gno_brno', 'ord_odno', 'psbl_qty']
            cf2 = ['종목코드', '주문수량', '주문단가', '주문일시', '주문구분', '주문번호', '주문가능수량']
            tdf = tdf[cf1]
            ren_dict = dict(zip(cf1, cf2))
            tdf.rename(columns=ren_dict, inplace=True)
            return tdf
        else:
            t1.print_error()
            return None
    
    def do_cancel_all_orders(self, skip_codes=[]):
        tdf = self.get_orders()
        if tdf is not None:
            od_list = tdf.index.to_list()
            qty_list = tdf['주문가능수량'].to_list()
            price_list = tdf['주문단가'].to_list()
            branch_list = tdf['주문구분'].to_list()
            codes_list = tdf['종목코드'].to_list()
            cnt = 0
            for x in od_list:
                if codes_list[cnt] in skip_codes:
                    continue
                ar = self.do_cancel_order(x, qty_list[cnt], price_list[cnt], branch_list[cnt])
                cnt += 1
                logger.info(f"Cancel Order: {ar}")
                time.sleep(0.02)

    # 해외 주식

    def get_current_price_overseas(self, exchange_code, stock_code):
        url = "/uapi/overseas-price/v1/quotations/price"
        tr_id = "HHDFS00000300"

        params = {
            "AUTH": "",
            "EXCD": exchange_code,
            "SYMB": stock_code,
        }

        t1 = self._url_fetch(url, tr_id, params)

        if t1 is not None and t1.is_ok():
            return t1.get_body().output
        else:
            t1.print_error()
            return None

    def get_account_balance_overseas(self):
        url = "/uapi/overseas-stock/v1/trading/inquire-balance"
        tr_id = "TTTS3012R"

        params = {
            "CANO": self.account_num,
            "ACNT_PRDT_CD": self.stock_account_product_code,
            "OVRS_EXCG_CD": "NASD",
            "TR_CRCY_CD": "USD",
            "CTX_AREA_FK200": "",
            "CTX_AREA_NK200": "",
        }

        t1 = self._url_fetch(url, tr_id, params)
        output_columns = ["종목코드", "해외거래소코드", "종목명", "보유수량", "매도가능수량", "매입단가", "수익률", "현재가", "평가손익"]
        
        if t1 is None:
            return 0, pd.DataFrame(columns=output_columns)
        
        try:
            output1 = t1.get_body().output1
        except Exception as e:
            logger.error(f"Error in get_account_balance_overseas: {e}")
            return 0, pd.DataFrame(columns=output_columns)
        
        if t1 is not None and t1.is_ok() and output1:
            df = pd.DataFrame(output1)
            
            target_columns = ["ovrs_pdno", "ovrs_excg_cd", "ovrs_item_name", "ovrs_cblc_qty", "ord_psbl_qty", "pchs_avg_pric", "evlu_pfls_rt", "now_pric2", "frcr_evlu_pfls_amt"]
            df = df[target_columns]
            df[target_columns[3:]] = df[target_columns[3:]].apply(pd.to_numeric)
            column_rename_map = dict(zip(target_columns, output_columns))
            df.rename(columns=column_rename_map, inplace=True)
            df = df[df['보유수량'] != 0]
            r2 = t1.get_body().output2
            return float(r2[0]['tot_evlu_pfls_amt']), df
        else:
            return 0, pd.DataFrame(columns=output_columns)
        
    def do_order_overseas(self, exchange_code, stock_code, price, quantity, order_type="00", prd_code="01", buy_flag=True):
        url = "/uapi/overseas-stock/v1/trading/order"

        if buy_flag:
            tr_id = "TTTT1002U"
        else:
            tr_id = "TTTT1006U"

        params = {
            "CANO": self.account_num,
            "ACNT_PRDT_CD": self.stock_account_product_code,
            "OVRS_EXCG_CD": exchange_code,
            "PDNO": stock_code,
            "ORD_QTY": str(quantity),
            "OVRS_ORD_UNPR": str(price),
            "ORD_SVR_DVSN_CD": "0",
            "ORD_DVSN": order_type,
        }

        t1 = self._url_fetch(url, tr_id, params, is_post=True, use_hash=True)

        if t1 is not None and t1.is_ok():
            return t1
        elif t1 is None:
            return None
        else:
            t1.print_error()
            return None
        
        
    def do_buy_order_overseas(self, exchange_code, stock_code, price, quantity, order_type="00", prd_code="01"):
        t1 = self.do_order_overseas(exchange_code, stock_code, price, quantity, order_type, prd_code, buy_flag=True)
        return t1

    def do_sell_order_overseas(self, exchange_code, stock_code, price, quantity, order_type="00", prd_code="01"):
        t1 = self.do_order_overseas(exchange_code, stock_code, price, quantity, order_type, prd_code, buy_flag=False)
        return t1

class APIResponse:
    def __init__(self, response):
        self.res_code = response.status_code
        self.resp = response
        self._header = self._set_header()
        self._body = self._set_body()
        self.error_code = self._body.rt_cd
        self.error_msg = self._body.msg1

    def get_result_code(self):
        return self.res_code

    def _set_header(self):
        fld = dict()
        for x in self.resp.headers.keys():
            if x.islower():
                fld[x] = self.resp.headers.get(x)
        _th_ = namedtuple('header', fld.keys())
        return _th_(**fld)
    
    def _set_body(self):
        _tb_ = namedtuple('body', self.resp.json().keys())
        return _tb_(**self.resp.json())
    
    def get_header(self):
        return self._header
    
    def get_body(self):
        return self._body
    
    def get_response(self):
        return self.resp

    def is_ok(self):
        try:
            if (self.get_body().rt_cd == '0'):
                return True
            else:
                return False
        except:
            return False
    
    def get_error_code(self):
        return self.error_code
    
    def get_error_msg(self):
        return self.error_msg
    
    def get_json(self):
        return self.resp.json()
    
    def get_status_code(self):
        return self.resp.status_code
    
    def print_all(self):
        logger.info("<Header>")
        for x in self.get_header()._fields:
            logger.info(f"{x}: {getattr(self._header, x)}")
        logger.info("<Body>")
        for x in self.get_body()._fields:
            logger.info(f"{x}: {getattr(self._body, x)}")
        
    def print_error(self):
        logger.error(f"Error In Response: {self.get_error_code()}")
        logger.error(f"Error Message: {self.get_error_msg()}")
