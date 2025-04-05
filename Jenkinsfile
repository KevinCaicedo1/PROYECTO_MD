pipeline {
    agent any

    environment {
        // Definir variables de entorno si es necesario, como tu entorno de Python
        VENV_DIR = "env"
    }

    stages {
        stage('Preparación del entorno') {
            steps {
                script {
                    // Crear y activar un entorno virtual
                    sh 'python -m venv $VENV_DIR'
                    sh './$VENV_DIR/Scripts/activate' // Para sistemas Windows, ajusta la ruta en Linux/Mac
                }
            }
        }

        stage('Instalación de dependencias') {
            steps {
                // Instalar las dependencias del proyecto
                script {
                    sh './$VENV_DIR/Scripts/activate && pip install -r requirements.txt'
                }
            }
        }

        stage('Ejecutar pruebas unitarias') {
            steps {
                script {
                    // Ejecutar las pruebas con pytest
                    sh './$VENV_DIR/Scripts/activate && pytest --maxfail=1 --disable-warnings -q'
                }
            }
        }

        stage('Generar cobertura de pruebas') {
            steps {
                script {
                    // Generar la cobertura de las pruebas
                    sh './$VENV_DIR/Scripts/activate && pytest --maxfail=1 --disable-warnings -q --cov=app --cov-report=html'
                }
            }
        }

        stage('Desplegar en entorno de producción') {
            when {
                branch 'main' // Ejecutar solo si estamos en la rama principal
            }
            steps {
                script {
                    // Aquí puedes colocar los pasos para el despliegue en producción (si es necesario)
                    echo "Desplegando aplicación..."
                    // Aquí puedes poner un comando como `docker build` o `docker-compose` si tu aplicación está en contenedores Docker
                }
            }
        }
    }

    post {
        always {
            // Pasos que deben ejecutarse siempre al final del pipeline (por ejemplo, limpieza)
            echo 'El pipeline ha terminado.'
        }

        success {
            // Pasos que deben ejecutarse solo si todo el pipeline fue exitoso
            echo 'Pipeline ejecutado con éxito.'
        }

        failure {
            // Pasos que deben ejecutarse solo si el pipeline falló
            echo 'Hubo un error en el pipeline.'
        }
    }
}
