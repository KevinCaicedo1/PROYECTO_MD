pipeline {
    agent {
        docker { 
            image 'python:3.9' // Usa una imagen de Python ya preparada
            args '-v /home/jenkins/workspace:/workspace' // Volumen para persistir datos
        }
    }

    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    echo 'Creando y activando el entorno virtual...'
                    sh 'python3 -m venv venv'
                    sh 'source venv/bin/activate'

                    echo 'Instalando dependencias...'
                    sh 'pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo 'Ejecutando pruebas unitarias...'
                    sh 'python3 -m unittest discover -s test'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo 'Desplegando aplicación...'
                    sh 'python app.py'
                }
            }
        }
    }
}
