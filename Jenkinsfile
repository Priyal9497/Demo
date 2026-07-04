pipeline {
    agent any

    environment {
        IMAGE_NAME = "priyal9497/employee-management"
        CONTAINER_NAME = "employee-management"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'python -m pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME% .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat '''
                    echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                    docker push %IMAGE_NAME%
                    '''
                }
            }
        }

        stage('Deploy Container') {
            steps {
                bat '''
                docker stop %CONTAINER_NAME%
                if %ERRORLEVEL% NEQ 0 echo Container not running.

                docker rm %CONTAINER_NAME%
                if %ERRORLEVEL% NEQ 0 echo Container does not exist.

                docker run -d --name %CONTAINER_NAME% -p 5000:5000 %IMAGE_NAME%
                '''
            }
        }
    }

    post {
        success {
            echo 'Deployment Successful!'
        }

        failure {
            echo 'Pipeline Failed!'
        }

        always {
            cleanWs()
        }
    }
}