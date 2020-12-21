pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh "docker-compose -p test_postgres up -d db"
                sh "docker-compose run --rm --name test_backend backend ./wait-for-it.sh db:5432"
                sh "docker-compose run --rm --name test_backend backend python manage.py makemigrations users"
                sh "docker-compose run --rm --name test_backend backend python manage.py migrate"
            }
        }
        stage('Test') {
            steps {
                // run test
                sh "docker-compose run --rm --name test_backend backend python manage.py test"
                // create report
                sh "docker-compose run --rm --name test_backend backend python manage.py jenkins"
                
            }
            
            post {
                always {
                    junit "reports/junit.xml"
                }
            }
        }
        stage('Clean up') {
            steps {
                sh "docker-compose down postgres"
                sh "docker-compose down"
            }
        }

        stage('Deploy') {
            steps {
                sh "cp README.md docs"
                sh "docker-compose up --build -d"
            }
        }
    }
}