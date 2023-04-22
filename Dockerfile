FROM python:3.10

COPY requirements.txt .

RUN pip install --user -r requirements.txt

ADD tgbot /tgbot_template/tgbot
ADD .env /tgbot_template/
ADD bot.py /tgbot_template/

WORKDIR /tgbot_template/

CMD ["python", "./bot.py"]

EXPOSE 8080
EXPOSE 8443
