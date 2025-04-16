FROM jenkins/jenkins:lts
USER root

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv git && apt-get clean

USER jenkins