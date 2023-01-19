FROM python:3.8

WORKDIR /usr/src/app
COPY ./code/requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./code/ /usr/src/app
CMD python3 /usr/src/app/vdb_main.py
