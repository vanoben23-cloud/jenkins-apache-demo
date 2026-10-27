
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
docker tag "$IMAGE_NAME:$IMAGE_TAG" "$REPO:$BUILD_NUMBER"
docker tag "$IMAGE_NAME:$IMAGE_TAG" "$REPO:latest"
docker images "$REPO"
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
docker push "$REPO:$BUILD_NUMBER"
docker push "$REPO:latest"
                    '''
                }
            }
}
    }
    post {
        success {
            echo 'SUCCESS: Docker image built!'
       
slackSend(
    channel: '#jenkins-alerts',
    color: 'good',
    message: "SUCCESS: ${env.JOB_NAME} Build #${env.BUILD_NUMBER} completed successfully! ${env.BUILD_URL}"
)
 }
        failure {
            echo 'FAILED: Check Jenkins Console Output.'
      
slackSend(
    channel: '#jenkins-alerts',
    color: 'danger',
    message: "FAILED: ${env.JOB_NAME} Build #${env.BUILD_NUMBER}. Check Jenkins: ${env.BUILD_URL}"
)
  }
    }
}

