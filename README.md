# Calculator Project

A small Python calculator that adds, subtracts and multiplies two **positive integers**.
It is packaged as a normal Python package and also deployed to AWS as a Lambda function
behind API Gateway, through a Jenkins CI/CD pipeline.

## Layout

```
src/calculator/operations.py   the maths + input validation
src/calculator/handler.py      Lambda handler (API Gateway events)
tests/                         pytest unit tests
template.yaml                  AWS SAM / CloudFormation template
Dockerfile                     build image used by Jenkins
Jenkinsfile                    pipeline (Docker agent)
Jenkinsfile.windows            fallback pipeline for Jenkins on Windows
docs/RUNBOOK.md                full setup steps + architecture
```

## Run the tests locally

```
pip install -r requirements-dev.txt
python -m pytest
```

## Build the package

```
python -m build
```
