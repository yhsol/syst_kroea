class OrderType:
    """주문 유형 상수"""
    LIMIT = "00"              # 지정가
    MARKET = "01"            # 시장가
    CONDITIONAL = "02"       # 조건부지정가
    BEST_LIMIT = "03"        # 최유리지정가
    FIRST_LIMIT = "04"       # 최우선지정가
    BEFORE_MARKET = "05"     # 장전 시간외
    AFTER_MARKET = "06"      # 장후 시간외
    SINGLE_PRICE = "07"      # 시간외 단일가
    TREASURY_STOCK = "08"    # 자기주식
    TREASURY_S_OPTION = "09" # 자기주식S-Option
    TREASURY_TRUST = "10"    # 자기주식금전신탁
    IOC_LIMIT = "11"         # IOC지정가
    FOK_LIMIT = "12"         # FOK지정가
    IOC_MARKET = "13"        # IOC시장가
    FOK_MARKET = "14"        # FOK시장가
    IOC_BEST = "15"          # IOC최유리
    FOK_BEST = "16"          # FOK최유리

    # 딕셔너리 형태로도 접근 가능
    TYPES = {
        "지정가": LIMIT,
        "시장가": MARKET,
        "조건부지정가": CONDITIONAL,
        "최유리지정가": BEST_LIMIT,
        "최우선지정가": FIRST_LIMIT,
        "장전 시간외": BEFORE_MARKET,
        "장후 시간외": AFTER_MARKET,
        "시간외 단일가": SINGLE_PRICE,
        "자기주식": TREASURY_STOCK,
        "자기주식S-Option": TREASURY_S_OPTION,
        "자기주식금전신탁": TREASURY_TRUST,
        "IOC지정가": IOC_LIMIT,
        "FOK지정가": FOK_LIMIT,
        "IOC시장가": IOC_MARKET,
        "FOK시장가": FOK_MARKET,
        "IOC최유리": IOC_BEST,
        "FOK최유리": FOK_BEST,
    } 