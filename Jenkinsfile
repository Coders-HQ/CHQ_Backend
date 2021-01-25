pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh "cp ../.env ."
                sh "rm -rf users/CHQ_Scoring/"
                sh "cd users"
                sh "git clone https://github.com/Coders-HQ/CHQ_Scoring.git"
                sh "cd .."
                sh "docker-compose run --rm web python manage.py test"
                sh "docker-compose run --rm web python manage.py jenkins"
                // create postgres
            }

        }
        stage('Test') {
            steps {
                // run test
                sh "docker-compose run --rm web python manage.py test"
                sh "docker-compose run --rm web python manage.py jenkins"
            }
            
            post {
                success {
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

        stage('Clean Up'){
            steps{
                // clean images
                // create postgres
                sh "docker stop test_postgres" 
                // create redis
                sh "docker stop test_redis" 
                // create celery
                sh "docker stop test_celery" 
                // create web
                sh "docker stop test_web" 
                sh "docker rm test_postgres" 
                // create redis
                sh "docker rm test_redis" 
                // create celery
                sh "docker rm test_celery" 
                // create web
                sh "docker rm test_web" 
            }
        }
    }
}