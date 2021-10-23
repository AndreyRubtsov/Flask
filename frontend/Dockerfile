FROM python:3.8
ARG TEST
ENV TEST2=$TEST
ENV ENV_RDS_HOST $TEST
ENV ENV_RDS_DB ${RDS_DB}
ENV ENV_RDS_USER ${DOCKER_USER}
ENV ENV_RDS_PASS 12
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD [ "python3", "./application.py"]
EXPOSE 5000
