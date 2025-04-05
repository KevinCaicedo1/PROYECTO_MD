pipeline {
    agent any

    environment {
        CONDA_DIR = "$HOME/miniconda3"
        ENV_NAME = "ml_env"
    }

    stages {
        stage('Install Miniconda') {
            steps {
                sh '''#!/bin/bash -e
                echo '🔧 Installing Miniconda...'

                export PATH="$CONDA_DIR/bin:$PATH"

                if [ ! -d "$CONDA_DIR" ]; then
                    curl -fsSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh
                    bash miniconda.sh -b -p $CONDA_DIR
                    rm miniconda.sh
                fi

                eval "$($CONDA_DIR/bin/conda shell.bash hook)"
                conda init bash
                '''
            }
        }

        stage('Create Conda Environment') {
            steps {
                sh '''#!/bin/bash -e
                export PATH="$CONDA_DIR/bin:$PATH"
                eval "$($CONDA_DIR/bin/conda shell.bash hook)"

                if ! conda env list | grep -q "$ENV_NAME"; then
                    conda create -n $ENV_NAME python=3.8 -y
                fi
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''#!/bin/bash -e
                echo '📦 Installing dependencies including compilers...'

                export PATH="$CONDA_DIR/bin:$PATH"
                eval "$($CONDA_DIR/bin/conda shell.bash hook)"
                conda activate $ENV_NAME

                # Herramientas para compilar scikit-surprise
                conda install -n $ENV_NAME -y cmake make gcc_linux-64 gxx_linux-64

                # Dependencias del proyecto
                conda install -n $ENV_NAME -y pandas flask scikit-learn

                # Usar pip para confluent-kafka y scikit-surprise
                conda run -n $ENV_NAME pip install --upgrade pip
                conda run -n $ENV_NAME pip install scikit-surprise confluent-kafka
                '''
            }
        }

        stage('Run Flask API') {
            steps {
                sh '''#!/bin/bash -e
                echo '🚀 Running Flask app...'

                export PATH="$CONDA_DIR/bin:$PATH"
                eval "$($CONDA_DIR/bin/conda shell.bash hook)"
                conda activate $ENV_NAME

                nohup python app.py &
                '''
            }
        }
    }
}
