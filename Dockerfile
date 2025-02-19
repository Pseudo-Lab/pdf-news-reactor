# Python 3.12 Slim 버전 사용
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# 환경 변수 설정 (모듈 경로 설정)
ENV PYTHONPATH=/app

# 필수 패키지 설치 (PostgreSQL 개발 라이브러리 추가)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 의존성 파일 복사 및 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# FastAPI 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
