pipeline {
    agent any
    environment {
        POETRY_VIRTUALENVS_IN_PROJECT = "true"
        APP_BUILD_ID = 0.1  // Força a criação do .venv na pasta do projeto
    }
    stages {
         stage('Build') {
            steps{
                echo "Build..."
                script {
                    sh "git branch"
                    try {
                        app = docker.build("etl:${env.APP_BUILD_ID}", "--network=host -f Dockerfile .")
                    } catch(err){
                        throw err
                    }
                }
            }
        }
        stage('Extract') {
            steps{
                echo "RUN..."
                script {
                    try {
                        sh "docker run --network=host -v ~/Development:/output etl:${env.APP_BUILD_ID} poetry run python3 src/etl/extract.py"
                    } catch(err) {
                        throw err
                    } finally {
                    }
                }
            }
        }
        stage('Transform (Leading)') {
            steps{
                echo "RUN..."
                script {
                    try {
                        sh "docker run --network=host -v ~/Development:/output etl:${env.APP_BUILD_ID} poetry run python3 src/etl/transform_leading.py"
                    } catch(err) {
                        throw err
                    } finally {
                    }
                }
            }
        }
        stage('Transform (Bronze)') {
            steps{
                echo "RUN..."
                script {
                    try {
                        sh "docker run --network=host -v ~/Development:/output etl:${env.APP_BUILD_ID} poetry run python3 src/etl/transform_bronze.py"
                    } catch(err) {
                        throw err
                    } finally {
                    }
                }
            }
        }
        stage('Transform (Silver)') {
            steps{
                echo "RUN..."
                script {
                    try {
                        sh "docker run --network=host -v ~/Development:/output etl:${env.APP_BUILD_ID} poetry run python3 src/etl/transform_silver.py"
                    } catch(err) {
                        throw err
                    } finally {
                    }
                }
            }
        }
        stage('Transform (Gold)') {
            steps{
                echo "RUN..."
                script {
                    try {
                        sh "docker run --network=host -v ~/Development:/output etl:${env.APP_BUILD_ID} poetry run python3 src/etl/transform_gold.py"
                    } catch(err) {
                        throw err
                    } finally {
                    }
                }
            }
        }
    }
}
