FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install flask requests

EXPOSE 5000

CMD ["python", "gateway.py"]
