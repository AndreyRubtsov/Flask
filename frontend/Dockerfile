FROM python:3.8
ENV ENV_RDS_HOST = ${RDS_HOST}
ENV ENV_RDS_DB = ${RDS_DB}
ENV ENV_RDS_USER = ${RDS_USER}
ENV ENV_RDS_PASS = ${RDS_PASS}
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD [ "python3", "./application.py"]
EXPOSE 5000
