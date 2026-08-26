FROM python:3.12-alpine

WORKDIR /home/myapp

RUN apk update && apk upgrade

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt && rm -rf /usr/local/lib/python3.12/site-packages/pip /usr/local/lib/python3.12/site-packages/pip-*.dist-info

COPY . .

EXPOSE 5050

CMD ["python3", "app.py"]