FROM python:3.11-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libjpeg-dev  \
    zlib1g-dev \
    poppler-utils \
    postgresql-client \
    supervisor \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install wheel
RUN pip install -r /app/requirements.txt
RUN pip install --force-reinstall channels==4.1.0
COPY . /app
WORKDIR /app
RUN mkdir -p /app/logs && \
    touch /app/logs/nginx-AutoFarm-info.log && \
    touch /app/logs/nginx-AutoFarm-info-nginx.log
COPY ./configs/crypto_tap.conf /etc/nginx/conf.d/default.conf
EXPOSE 80