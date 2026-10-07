# Image used by the Jenkins pipeline.
# Python 3.12 matches the Lambda runtime in template.yaml, so what passes
# the tests here is what actually runs in AWS.
FROM python:3.12-slim
ENV HOME=/tmp PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN pip install --no-cache-dir pytest build awscli aws-sam-cli

# The project code is mounted into /app at run time (Jenkins does this for us),
# e.g.  docker run --rm -v "%cd%:/app" calculator-ci
CMD ["python", "-m", "pytest", "-v"]
