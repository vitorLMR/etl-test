pipeline {
    agent any
    environment {
        POETRY_VIRTUALENVS_IN_PROJECT = "false"  // Força a criação do .venv na pasta do projeto
    }
    stages {
        stage('Setup Environment') {
            steps {
                sh '''
                # Instalar Poetry se não existir
                pip3 install poetry==1.4.0
                
                poetry config virtualenvs.in-project false
                
                poetry export -f requirements.txt --without-hashes > requirements.txt
                pip install -r requirements.txt
                '''
            }
        }
        stage('Extract') {
            steps {
                sh 'python3 src/etl/extract.py'
            }
        }
        stage('Transform (Leading)') {
            steps {
                sh 'python3 src/etl/transform_leading.py'
            }
        }
        stage('Transform (Bronze)') {
            steps {
                sh 'python3 src/etl/transform_bronze.py'
            }
        }
        stage('Transform (Silver)') {
            steps {
                sh 'python3 src/etl/transform_silver.py'
            }
        }
        stage('Load') {
            steps {
                sh 'python3 src/etl/load.py'
            }
        }
    }
}
