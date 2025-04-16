pipeline {
    agent any
    stages {
        stage('Checkout Git') {
            steps {
                git 'https://github.com/anuranjan7892/SwagLabs.git'
            }
        }
        stage('Deploy to Test'){
            steps {
                sh 'chmod +x deploy/test_deploy.sh'
                sh './deploy/test_deploy.sh'
            }
        }
        stage('Environment setup') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Run smoke tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest -m smoke --html=report.html --self-contained-html'
                '''
            }
        }
        stage('Deploy to Production'){
            steps {
                input message: 'Proceed to Production?'
                sh 'chmod +x deploy/prod_deploy.sh'
                sh './deploy/prod_deploy.sh'
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true

            publishHTML(target: [
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: '.',
                reportFiles: 'report.html',
                reportName: 'Pytest Report'
            ])
        }
    }
}