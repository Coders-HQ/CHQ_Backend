pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh "cp ../.env ."
                sh "docker-compose -p test_backend run --rm  web ./wait-for-it.sh db:5432"
                sh "docker-compose -p test_backend run --rm  web python manage.py makemigrations users"
                sh "docker-compose -p test_backend run --rm  web python manage.py migrate"
            }
        }
        stage('Test') {
            steps {
                // run test
                sh "docker-compose -p test_backend run --rm  web python manage.py test"
                // create report
                sh "docker-compose -p test_backend run --rm  web python manage.py jenkins"
                
            }
            
            post {
                always {
                    // save report
                    junit "reports/junit.xml"
                }
            }
        }
        // stage('Prepare Deploy') {
        //     when { branch "main" }
        //     steps {
        //         sh "docker-compose down"
        //     }
        // }

        // stage('Deploy') {
        //     when { branch "main" }
        //     steps {
        //         sh "cp README.md docs"
        //         sh "docker-compose up --build -d"
        //     }
        // }

        // stage('Clean Up'){
        //     steps{
        //         // clean images
        //         sh "docker system prune -f"
        //     }
        // }
    }
}