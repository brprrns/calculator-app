pipeline {
    agent any

    triggers { githubPush() }

    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 25, unit: 'MINUTES')
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
    }

    post {
        success { echo 'CI succeeded' }
        failure { echo 'CI failed, check the stage logs above' }
    }
}
