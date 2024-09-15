FROM python:3.12.5

WORKDIR /usr/bot/

COPY ./requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . ./

ENV PYTHONPATH=/usr/bot/src

ENTRYPOINT ["python", "src/main.py"]