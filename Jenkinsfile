pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                bat '''
                if not exist venv python -m venv venv
                venv\\Scripts\\pip install --upgrade pip
                venv\\Scripts\\pip install -r requirements.txt
                '''
            }
        }

        stage('Run Automated Tests (CI Enhancement)') {
            steps {
                bat '''
                venv\\Scripts\\pytest -v
                '''
            }
        }

        stage('Build Artifact') {
            steps {
                bat '''
                venv\\Scripts\\python -m build
                '''
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: 'dist/*', fingerprint: true
        }
    }
}