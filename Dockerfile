FROM python:3.8
COPY frontend /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD [ "python3", "./application.py"]
EXPOSE 5000
