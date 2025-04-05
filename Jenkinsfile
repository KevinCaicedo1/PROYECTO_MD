pipeline {
    agent any  // Puedes usar cualquier agente aquí

    environment {
        VIRTUAL_ENV = 'venv'  // Nombre del entorno virtual
    }

    stages {
        stage('Install Python and Dependencies') {
            steps {
                script {
                    // Verificar que la imagen de Docker tiene Python instalado
                    echo 'Verificando la versión de Python...'
                    sh 'python3 --version'

                    // Crear entorno virtual y activar
                    echo 'Creando y activando el entorno virtual...'
                    sh 'python3 -m venv ${VIRTUAL_ENV}'
                    sh 'source ${VIRTUAL_ENV}/bin/activate'

                    // Instalar dependencias desde requirements.txt
                    echo 'Instalando dependencias...'
                    sh './${VIRTUAL_ENV}/bin/pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo 'Ejecutando pruebas unitarias...'
                    // Ejecutar las pruebas, si tienes un archivo de pruebas configurado
                    sh './${VIRTUAL_ENV}/bin/python -m unittest discover -s test'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Puedes agregar aquí los pasos de despliegue o continuar con otros pasos de tu pipeline
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
            // Puedes realizar tareas de limpieza si es necesario
            sh 'deactivate'
        }
    }
}
