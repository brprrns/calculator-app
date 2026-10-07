// CI/CD pipeline for the calculator project.
//
// Everything runs inside a Docker container built from the Dockerfile in this
// repo, so each build gets the same Python + SAM CLI no matter what is
// installed on the Jenkins machine.
//
// Needs in Jenkins:
//   - Docker Pipeline plugin
//   - a credential called "aws-creds" (Username with password:
//     username = AWS access key id, password = AWS secret access key)

pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile'
            args '-u root'
        }
    }

    triggers {
        githubPush()
    }

    options {
        disableConcurrentBuilds()
    }

    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'
        STACK_NAME         = 'calculator-stack'
        SAM_CLI_TELEMETRY  = '0'
    }

    stages {
        // ---------- CI ----------
        stage('Unit tests') {
            steps {
                sh 'python -m pytest -v'
            }
        }

        stage('Build package') {
            steps {
                sh 'python -m build'
                archiveArtifacts artifacts: 'dist/*', fingerprint: true
            }
        }

        stage('SAM build') {
            steps {
                sh 'sam build'
            }
        }

        // ---------- CD ----------
        stage('Deploy to AWS') {
            // only deploy what lands on main, other branches just get tested
            when {
                expression { env.GIT_BRANCH == 'origin/main' || env.BRANCH_NAME == 'main' }
            }
            steps {
                withCredentials([usernamePassword(
                        credentialsId: 'aws-creds',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh '''
                        sam deploy \
                          --stack-name $STACK_NAME \
                          --resolve-s3 \
                          --capabilities CAPABILITY_IAM \
                          --no-confirm-changeset \
                          --no-fail-on-empty-changeset

                        echo "---- Stack outputs ----"
                        sam list stack-outputs --stack-name $STACK_NAME
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline finished OK.'
        }
        failure {
            echo 'Pipeline failed - check the stage that went red above.'
        }
    }
}
