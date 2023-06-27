# Requirements
- python 3.9

# Setup
```shell
pip install -r requirements.txt
```

# Run the project
```shell
export FLASK_APP="/Users/wentungwen/Desktop/keto_app/main.py"
source var.sh
flask run --port=5001 --reload
```


# Deactivate/activate environment
It is suggested to use Anaconda managing and building the environment.

- Create the environments.
```shell
conda create -n keto python=3.9
```

- Activate/deactivate environments.
```shell
conda activate keto
conda deactivate
```

- Show and remove the environment.
```shell
conda env list 
conda remove --name 5_8_amazon  --all
```

