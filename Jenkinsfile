pipeline {
    agent any
    environment {
        POETRY_VIRTUALENVS_IN_PROJECT = "true"  // Força a criação do .venv na pasta do projeto
    }
    stages {
        stage('Setup Environment') {
            steps {
                sh '''
                # Instalar Poetry se não existir
                if ! command -v poetry &> /dev/null; then
                    curl -sSL https://install.python-poetry.org | python3 -
                    echo "export PATH=$HOME/.local/bin:$PATH" >> ~/.bashrc
                    . ~/.bashrc
                fi
                
                poetry config virtualenvs.in-project true
                
                poetry install --no-interaction

                . $(poetry env info --path)/bin/activate
                '''
            }
        }
        stage('Extract') {
            steps {
                sh 'poetry run python src/etl/extract.py'
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
