FROM python:3.12.5

WORKDIR /usr/bot/

COPY ./requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/usr/bot/src

#RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip && \
#    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
#    rm /tmp/chromedriver.zip

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    libgconf-2-4 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxtst6 \
    libnss3 \
    libxrandr2 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libpangocairo-1.0-0 \
    libcups2 \
    libgbm1 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    --no-install-recommends

# Устанавливаем Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update && apt-get install -y google-chrome-stable

# Устанавливаем ChromeDriver
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

COPY . ./

ENTRYPOINT ["python", "src/main.py"]