FROM python:3.11

RUN addgroup --gid 10001 api_user && \
    adduser --uid 10001 --gid 10001 --disabled-password --gecos "" api_user

WORKDIR /usr/backend/embeddings

COPY --chown=api_user:api_user ./requirements.txt .

RUN pip install --no-cache-dir torch && \
    pip install --no-cache-dir -r requirements.txt

COPY --chown=api_user:api_user . ./

ENV PYTHONPATH=/usr/backend

USER api_user

ENTRYPOINT ["python", "api.py"]