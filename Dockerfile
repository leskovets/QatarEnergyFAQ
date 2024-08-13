FROM python:3.12.1

RUN apt -y update
RUN apt -y upgrade

COPY requirements.txt ./app/

WORKDIR /app

RUN python -m pip install -r requirements.txt

COPY . /app/

ENTRYPOINT ["python", "main.py"]
