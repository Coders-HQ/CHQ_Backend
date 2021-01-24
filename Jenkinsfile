pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh "cp ../.env ."
                // create postgres
                sh "docker-compose run --no-deps --name test_postgres -d db" 
                // create redis
                sh "docker-compose run --no-deps --name test_redis -d redis" 
                // create celery
                sh "docker-compose run --no-deps --name test_celery -d celery" 
                // create web
                sh "docker-compose run --no-deps --name test_web -d web" 
                // make sure connection is made
                sh "docker-compose run --rm --no-deps --name test_backend web ./wait-for-it.sh db:5432"
                // migration data to postgres
                sh "docker-compose run --rm --no-deps --name test_backend web python manage.py makemigrations users"
                sh "docker-compose run --rm --no-deps --name test_backend web python manage.py migrate"
            }
        }
        stage('Test') {
            steps {
                // run test
                sh "docker-compose run --rm --no-deps --name test_backend web python manage.py test"
                // create report
                sh "docker-compose run --rm --no-deps --name test_backend web python manage.py jenkins"
                
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