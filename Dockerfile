FROM python:3.7.4-slim

RUN apt-get update \
    && apt-get install graphviz -y \
    && apt-get clean

RUN pip install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt                                                                            

EXPOSE 5000

CMD ["python", "main.py"]