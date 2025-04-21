pipeline {
    agent any

    tools {
        // Use the same name you gave in the Allure tool config
        allure 'Allure CLI'
    }
    
    stages {
        stage('Checkout Git') {
            steps {
                git 'https://github.com/anuranjan7892/SwagLabs.git'
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
        stage('Dev code changes') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest -k test_add_new_change
                '''
            }
        }
        stage('Deploy to Test'){
            steps {
                sh 'chmod +x deploy/test_deploy.sh'
                sh './deploy/test_deploy.sh'
            }
        }
        stage('Run smoke tests') {
            steps {
                script {
                    try {
                        sh '''
                            . venv/bin/activate
                            pytest -m smoke --html=report.html --self-contained-html
                        '''
                    } catch (err) {
                        currentBuild.result = 'FAILURE'
                        error("Smoke tests failed. Stopping CI CD pipeline: ${err}")
                    }
                }
            }
        }
        stage('Deploy to Production'){
            steps {
                sh 'chmod +x deploy/prod_deploy.sh'
                sh './deploy/prod_deploy.sh'
            }
        }
    }
    post {
        always {
            // Generate HTML report
        sh '''
            allure generate allure-results --clean -o allure-report
        '''

        // Publish Allure in Jenkins UI
        allure([
            includeProperties: false,
            jdk: '',
            results: [[path: 'allure-results']]
        ])

        // Archive HTML report as artifact
        archiveArtifacts artifacts: 'allure-report/**', fingerprint: true
        }
    }
}
