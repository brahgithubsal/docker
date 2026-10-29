pipeline {
    agent any

    environment {
        IMAGE_NAME = 'flask-task-app'
        IMAGE_TAG  = "v${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Recuperation du code depuis GitHub...'
                checkout scm
            }
        }

        stage('Lint & Qualite') {
            steps {
                echo 'Verification de la syntaxe Python...'
                sh 'python3 -m py_compile src/app.py && echo "Syntaxe OK ✅"'
            }
        }

        stage('Docker Build') {
            steps {
                echo "Construction de l image ${IMAGE_NAME}:${IMAGE_TAG}..."
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "docker images ${IMAGE_NAME}"
            }
        }

        stage('Deploy Staging') {
            steps {
                sh """
                    docker rm -f staging-flask-app || true
                    docker run -d --name staging-flask-app -p 5001:5000 ${IMAGE_NAME}:${IMAGE_TAG}
                    sleep 3
                    curl -sf http://localhost:5001/health && echo 'Health check OK ✅'
                """
            }
        }

        stage('Cleanup') {
            steps {
                sh 'docker rm -f staging-flask-app || true'
                echo 'Nettoyage termine ✅'
            }
        }
    }

    post {
        success { echo "✅ Pipeline reussi ! Image ${IMAGE_NAME}:${IMAGE_TAG} prete." }
        failure { echo "❌ Pipeline echoue. Consultez les logs ci-dessus." }
    }
}