
pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }
    parameters {
        string(
            name: 'IMAGE_TAG',
            defaultValue: 'latest',
            description: 'Enter Docker image version'
        )

        string(
            name: 'IMAGE_NAME',
            defaultValue: 'class28-app',
            description: 'Enter Docker image name'
        )
   }

environment {
    REPO = 'vanessadevopslady/class_28_repo'
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
                   docker build -t "$IMAGE_NAME:$IMAGE_TAG" .
                    docker images class28-app
                '''
            }
        }
    stage('Scan Docker Image') {
    steps {
        sh 'trivy image --scanners vuln --exit-code 1 --severity HIGH,CRITICAL "$IMAGE_NAME:$IMAGE_TAG"'
    }
}


         stage('Tag Docker Image') {
    steps {
        sh '''
           docker tag "$IMAGE_NAME:$IMAGE_TAG" "$REPO:$IMAGE_TAG"
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

                        docker push "$REPO:$IMAGE_TAG"
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

