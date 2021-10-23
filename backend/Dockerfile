FROM python:3.8
ARG ENV_RDS_HOST=$RDS_HOST
ARG ENV_RDS_DB=$RDS_DB
ARG ENV_RDS_USER=$RDS_USER
ARG ENV_RDS_PASS=$RDS_PASS
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD [ "python3", "./backend.py"]
EXPOSE 5000
