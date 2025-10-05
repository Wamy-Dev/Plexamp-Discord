FROM python:3.10-alpine
WORKDIR /app

RUN apk add --no-cache python3 python3-dev openssl bash nano

COPY requirements.txt .
RUN pip --no-cache-dir install -U -r requirements.txt
COPY . .

ENTRYPOINT [ "python", "main.py" ]