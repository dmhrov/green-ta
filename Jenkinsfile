pipeline {
    agent any
    
    environment {
        IMAGE_NAME = "simple-python-app:${BUILD_NUMBER}"
        CONTAINER_NAME = "simple-python-app"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }
        
        stage('Run Tests') {
            steps {
                sh """
                docker run -d --name test-app -p 5000:5000 ${IMAGE_NAME}
                sleep 35  # Wait for container to start
                docker run --rm --network host -e APP_HOST=localhost -e APP_PORT=5000 \
                    -v \$(pwd)/test_app.py:/test_app.py python:3.9-slim \
                    bash -c "pip install requests && python /test_app.py"
                """
            }
            post {
                always {
                    sh "docker stop test-app || true"
                    sh "docker rm test-app || true"
                }
            }
        }
        
        stage('Deploy') {
            steps {
                sh """
                export IMAGE_NAME=${IMAGE_NAME}
                docker-compose down || true
                docker-compose up -d
                """
            }
        }
        
        stage('Verify Deployment') {
            steps {
                sh "curl -f http://localhost:5000/health"
            }
        }
    }
    
    post {
        failure {
            echo 'Pipeline failed!'
        }
        success {
            echo 'Pipeline succeeded!'
        }
        always {
            sh "docker ps"
        }
    }
}