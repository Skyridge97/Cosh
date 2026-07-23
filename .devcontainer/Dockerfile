FROM mcr.microsoft.com/vscode/devcontainers/python:3.9

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -N http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    chmod +x chromedriver && \
    mv -f chromedriver /usr/local/share/chromedriver-linux64/chromedriver && \
    ln -s /usr/local/share/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    ln -s /usr/local/share/chromedriver-linux64/chromedriver /usr/bin/chromedriver

# Install xvfb (for headless operation)
RUN apt-get update && apt-get install -y xvfb

# Set display for xvfb
ENV DISPLAY=:99
