# Korea Investment Trading System

한국투자증권 OpenAPI를 활용한 주식 트레이딩 시스템입니다. 국내 주식과 해외 주식 거래를 모두 지원합니다.

## 기능

### 국내 주식

- 계좌 잔고 조회
- 현재가 조회
- 호가 정보 조회
- 등락률 순위 조회
- 주문 (매수/매도)
- 주문 취소
- 주문 내역 조회

### 해외 주식

- 계좌 잔고 조회
- 현재가 조회
- 주문 (매수/매도)

## 설치 방법

1. Python 환경 설정:
   - conda create -n koreainvest python=3.9
   - conda activate koreainvest
2. 패키지 설치:

   - pip install -r requirements.txt

3. 설정 파일 생성:
   `config.yaml` 파일을 프로젝트 루트 디렉토리에 생성하고 다음 내용을 입력하세요:

```yaml
api_key: "your-api-key"
api_secret_key: "your-api-secret-key"
stock_account_number: "your-account-number"
stock_account_product_code: ""
hts_id: "your-hts-id"
custtype: ""
is_paper_trading: False
my_agent: "Mozilla/5.0..."
url: "https://openapi.koreainvestment.com:xxxx"
```

## 실행 방법

1. Conda 환경 활성화:

```bash
conda activate koreainvest
```

2. 서버 실행:

```bash
uvicorn app.main:app --reload
```

## API 엔드포인트

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 개발 환경

- Python 3.9
- FastAPI
- Pandas
- PyYAML
- 기타 의존성은 requirements.txt 참조

## 주의사항

- API 키와 시크릿은 절대 GitHub에 커밋하지 마세요
- 실제 거래 전에 반드시 테스트를 충분히 진행하세요
- 거래소 규정과 API 사용량 제한을 준수하세요
