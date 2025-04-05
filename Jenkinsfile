pipeline {
    agent any  // Puedes usar cualquier agente aquí

    environment {
        VIRTUAL_ENV = 'venv'  // Nombre del entorno virtual
    }

    stages {
        stage('Install Python') {
            steps {
                script {
                    echo 'Verificando si Python está instalado...'
                    
                    // Comprobamos si Python está instalado
                    def pythonCheck = sh(script: 'python3 --version', returnStatus: true)
                    
                    // Si Python no está instalado, instalamos desde una fuente
                    if (pythonCheck != 0) {
                        echo 'Python no está instalado. Instalando Python...'

                        // Actualizamos los paquetes
                        sh 'apt-get update -y'
                        
                        // Instalar Python 3 y las herramientas necesarias
                        sh 'apt-get install -y python3 python3-pip python3-venv'
                    } else {
                        echo 'Python ya está instalado.'
                    }

                    // Verificar la instalación de Python
                    sh 'python3 --version'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    echo 'Creando y activando el entorno virtual...'
                    sh 'python3 -m venv ${VIRTUAL_ENV}'
                    sh 'source ${VIRTUAL_ENV}/bin/activate'

                    echo 'Instalando dependencias...'
                    sh './${VIRTUAL_ENV}/bin/pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo 'Ejecutando pruebas unitarias...'
                    sh './${VIRTUAL_ENV}/bin/python -m unittest discover -s test'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo 'Desplegando aplicación...'
                    // Por ejemplo, si necesitas lanzar la aplicación Flask
                    sh './${VIRTUAL_ENV}/bin/python app.py'
                }
            }
        }
    }

    post {
        always {
            echo 'Limpieza después del pipeline'
            sh 'deactivate'
        }
    }
}
