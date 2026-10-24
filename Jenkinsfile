
pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    stages {
        stage('Checkout Git Repository') {
            steps {
                git branch: 'release/v1.0.0',
                    url: 'https://github.com/vanoben23-cloud/jenkins-apache-demo.git'
            }
        }

        stage('Verify Git Checkout') {
            steps {
                sh '''
                    echo "Current Directory:"
                    pwd

                    echo "Repository Files:"
                    ls -la

                    echo "Git Branches:"
                    git branch -a

                    echo "Checking Application Files:"
                    test -f Dockerfile
                    test -f app.py
                    test -f requirements.txt
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker --version
                    docker build -t class28-app:latest .
                    docker images class28-app
                '''
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Docker image built!'
        }
        failure {
            echo 'FAILED: Check Jenkins Console Output.'
        }
    }
}

