FROM python:3.12-slim
WORKDIR /home/myapp
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5050
CMD ["python3", "app.py"]

