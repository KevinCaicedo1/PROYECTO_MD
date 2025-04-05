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
                    echo '🚀 Downloading and installing Miniconda...'
                    curl -fsSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh
                    bash miniconda.sh -b -p $CONDA_DIR
                    rm miniconda.sh
                    echo '✅ Miniconda installed successfully!'
                else
                    echo '✅ Miniconda is already installed.'
                fi

                eval "$($CONDA_DIR/bin/conda shell.bash hook)"
                conda init bash
                '''
            }
        }

        stage('Create Conda Environment') {
            steps {
                sh '''#!/bin/bash -e
                echo '🌱 Creating and activating Conda environment...'

                export PATH="$CONDA_DIR/bin:$PATH"
                eval "$($CONDA_DIR/bin/conda shell.bash hook)"

                if ! conda env list | grep -q "$ENV_NAME"; then
                    conda create -n $ENV_NAME python=3.8 -y
                    echo '✅ Conda environment created!'
                else
                    echo '✅ Conda environment already exists.'
                fi
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''#!/bin/bash -e
                echo '📦 Installing project dependencies...'

                export PATH="$CONDA_DIR/bin:$PATH"
                eval "$($CONDA_DIR/bin/conda shell.bash hook)"
                conda activate $ENV_NAME

                # Instalar dependencias con conda
                conda install -n $ENV_NAME -y pandas flask scikit-learn

                # Instalar dependencias específicas con pip (más confiable para estos paquetes)
                conda run -n $ENV_NAME pip install scikit-surprise confluent-kafka

                echo '✅ Dependencies installed.'
                '''
            }
        }

        stage('Run Flask API') {
            steps {
                sh '''#!/bin/bash -e
                echo '🚀 Starting Flask application...'

                export PATH="$CONDA_DIR/bin:$PATH"
                eval "$($CONDA_DIR/bin/conda shell.bash hook)"
                conda activate $ENV_NAME

                nohup python app.py &

                echo '✅ Flask API started.'
                '''
            }
        }
    }
}
