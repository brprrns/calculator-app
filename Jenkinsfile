pipeline {
    agent any

    triggers { githubPush() }

    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
    }

    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'
        STACK_NAME         = 'calculator-app'
    }

    stages {
        stage('Build Docker agent image') {
            steps { bat 'docker build -t calc-ci .' }
        }
        stage('CI - Unit tests') {
            steps { bat 'docker run --rm -v "%WORKSPACE%:/app" -w /app calc-ci python -m pytest -v' }
        }
        stage('CI - Build package') {
            steps { bat 'docker run --rm -v "%WORKSPACE%:/app" -w /app calc-ci sam build' }
        }
        stage('CD - Deploy to AWS') {
            when { expression { env.GIT_BRANCH == 'origin/main' } }
            steps {
                withCredentials([
                    string(credentialsId: 'aws-access-key-id', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-access-key', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    bat 'docker run --rm -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_DEFAULT_REGION -v "%WORKSPACE%:/app" -w /app calc-ci sam deploy --stack-name %STACK_NAME% --region %AWS_DEFAULT_REGION% --resolve-s3 --capabilities CAPABILITY_IAM --no-confirm-changeset --no-fail-on-empty-changeset'
                }
            }
        }
        stage('Smoke test') {
            when { expression { env.GIT_BRANCH == 'origin/main' } }
            steps {
                withCredentials([
                    string(credentialsId: 'aws-access-key-id', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-access-key', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    bat 'docker run --rm -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_DEFAULT_REGION -v "%WORKSPACE%:/app" -w /app calc-ci python smoke_test.py'
                }
            }
        }
    }

    post {
        success { echo 'Pipeline succeeded: tested, built and deployed' }
        failure { echo 'Pipeline failed, check the stage logs above' }
    }
}
