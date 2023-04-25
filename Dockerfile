FROM python:3.10.7

WORKDIR /src

COPY req.txt /src/req.txt

RUN pip install --no-cache-dir --upgrade -r req.txt

COPY . /src

CMD ["python3", "bot03.py"]