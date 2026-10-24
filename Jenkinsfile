
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
    

    
        stage('Scan Docker Image') {
            steps {
                sh '''
                trivy --config="" image --scanners vuln --exit-code 1 --severity HIGH,CRITICAL class28-app:latest
                '''
            }
        }

         stage('Tag Docker Image') {
    steps {
        sh '''
            docker tag class28-app:latest vanessadevopslady/class_28_repo:latest
            docker images vanessadevopslady/class_28_repo
        '''
    }
}
        stage('Push Docker Image to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_HUB_USER',
                        passwordVariable: 'DOCKER_HUB_TOKEN'
                    )
                ]) {
                    sh '''
                        set -e
                        set +x

                        export DOCKER_CONFIG="$(mktemp -d)"
                        trap 'rm -rf "$DOCKER_CONFIG"' EXIT

                        printf '%s' "$DOCKER_HUB_TOKEN" |
                          docker login -u "$DOCKER_HUB_USER" --password-stdin

                        docker push vanessadevopslady/class_28_repo:latest
                    '''
                }
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

