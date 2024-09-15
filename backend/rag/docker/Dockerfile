FROM python:3.11

RUN addgroup --gid 10001 api_user && \
    adduser --uid 10001 --gid 10001 --disabled-password --gecos "" api_user

WORKDIR /usr/backend/rag/

COPY --chown=api_user:api_user ./requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY --chown=api_user:api_user . ./

ENV PYTHONPATH=/usr/backend/

USER api_user

ENTRYPOINT ["python", "src/main.py"]