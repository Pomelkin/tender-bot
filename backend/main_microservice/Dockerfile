FROM python:3.12.5

RUN addgroup --gid 10001 api_user && \
    adduser --uid 10001 --gid 10001 --disabled-password --gecos "" api_user

WORKDIR /usr/main_microserivce/

COPY --chown=api_user:api_user ./requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY --chown=api_user:api_user . ./

ENV PYTHONPATH=/usr/main_microserivce/src

USER api_user
#ENTRYPOINT ["tail", "-f", "/dev/null"]

ENTRYPOINT ["python", "src/application/api/main.py"]
