FROM python:3.12-slim
ENV HOME=/tmp PIP_DISABLE_PIP_VERSION_CHECK=1
RUN pip install --no-cache-dir pytest awscli aws-sam-cli