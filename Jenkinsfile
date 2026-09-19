pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile'
            args '-u root'
        }
    }

    triggers { githubPush() }

    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 20, unit: 'MINUTES')
    }

    stages {
        stage('CI - Unit tests') {
            steps { sh 'pytest -v --junitxml=test-results.xml' }
            post { always { junit 'test-results.xml' } }
        }

        stage('CI - Build package') {
            steps { sh 'sam build' }
        }
    }

    post {
        success { echo 'CI succeeded' }
        failure { echo 'CI failed, check the stage logs above' }
    }
}