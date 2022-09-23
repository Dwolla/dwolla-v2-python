FROM python:3.7

WORKDIR /dwollav2

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "setup.py", "test"]
