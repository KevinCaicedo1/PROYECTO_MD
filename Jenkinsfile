pipeline {
    agent any

    stages {
        stage('Install Python') {
            steps {
                script {
                    echo 'Instalando Python desde el código fuente...'

                    // Descargar el código fuente de Python
                    sh 'wget https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz'

                    // Extraer el archivo
                    sh 'tar -xzf Python-3.9.6.tgz'

                    // Compilar Python
                    sh 'cd Python-3.9.6 && ./configure --prefix=$HOME/python && make && make install'

                    // Agregar el directorio de binarios a la variable de entorno PATH
                    sh 'export PATH=$HOME/python/bin:$PATH'

                    // Verificar la instalación
                    sh '$HOME/python/bin/python3 --version'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    echo 'Creando y activando el entorno virtual...'
                    sh '$HOME/python/bin/python3 -m venv venv'
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
