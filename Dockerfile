FROM jenkins/jenkins:lts

USER root

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv git wget curl unzip gnupg2 software-properties-common \
    libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 libxss1 libappindicator1 \
    libasound2 libxtst6 libxrandr2 libxcomposite1 libatk-bridge2.0-0 libgtk-3-0 \
    libxdamage1 libxfixes3 libxext6 libx11-xcb1 libxcb1 libx11-6 libxau6 libxdmcp6 libgbm1 \
    fonts-liberation lsb-release xdg-utils ca-certificates && \
    \
    # Install Allure CLI
    wget https://github.com/allure-framework/allure2/releases/download/2.25.0/allure-2.25.0.zip && \
    unzip allure-2.25.0.zip -d /opt/ && \
    ln -s /opt/allure-2.25.0/bin/allure /usr/bin/allure && \
    rm -rf allure-2.25.0.zip && \
    allure --version

# ----------------------------------------
# Install Google Chrome
# ----------------------------------------
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# ----------------------------------------
# Install Firefox and GeckoDriver
# ----------------------------------------
RUN apt-get install -y firefox-esr

# Install jq for parsing JSON (used for getting latest geckodriver version)
RUN apt-get install -y jq

# Install GeckoDriver (for Firefox automation with Selenium)
RUN GECKO_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | jq -r .tag_name) && \
    wget -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/$GECKO_VERSION/geckodriver-$GECKO_VERSION-linux64.tar.gz && \
    tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm /tmp/geckodriver.tar.gz

# ----------------------------------------
# Install Microsoft Edge (Chromium-based)
# ----------------------------------------
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg && \
    install -o root -g root -m 644 microsoft.gpg /usr/share/keyrings/ && \
    sh -c 'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge.list' && \
    apt-get update && apt-get install -y microsoft-edge-stable && \
    rm microsoft.gpg

USER jenkins
