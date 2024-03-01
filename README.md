# Reinforcement learning environment for Configuration AgreementMakerLight

This repository contains a simple reinforcement learning environment designed to find optimal configurations using the AgreementMakerLight library.

## File Structure
```

├── RL_Train_Example.ipynb # Jupyter notebook for training
├── AML
│ │── store
│ │ ├── config.py # Configuration settings
│ │ ├── config_original.py # Configuration settings
│ │ ├── AgreementMakerLights files.
│ ├── AgreementMakerLight.jar 
│── environment.py # RL environment implementation
│── config_edit.py # Agents' actions to configuration
│── connector.py # Load AgreementMakerLight.jar
│── test_connector.py # Testing AgreementMakerLight execution
├── README.md # Project README file
├── LICENSE.txt # License file
└── requirements.txt # Dependencies
```

## Installation

1. Clone this repository to your local machine:
2. Install the dependencies:
```bash
pip install -r requirements.txt
```

## Usage
Training: Open and execute the Jupyter notebook RL_Train_Example.ipynb to train the agent.

# License

This project is licensed under the MIT License - see the LICENSE file for details.