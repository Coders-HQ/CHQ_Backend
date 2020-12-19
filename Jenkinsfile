pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh "docker-compose run --rm backend ./wait-for-it.sh db:5432"
                sh "docker-compose run --rm backend python manage.py makemigrations users"
                sh "docker-compose run --rm backend python manage.py migrate"
            }
        }
        stage('Test') {
            steps {
                // run test
                sh "docker-compose run --rm backend python manage.py test"
                // create report
                sh "docker-compose run --rm backend python manage.py jenkins"
                
            }
            
            post {
                always {
                    junit "reports/junit.xml"
                }
            }
        }
        stage('Clean up') {
            steps {
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