# aws_lambdas
AWS Lambdas Repo

Steps to make zip of any repo to upload in Aws Lambda

1. Cd into Respective folder
2. Install virtualenv (python3 -m pip install virtualenv)
3. Create virtualenv (python3 -m venv {name of your venv})
4. Activate virtualenv (source {name of your venv}/bin/activate)
5. pip install -r requirements.txt
6. Make required changes in lambda_funcation.py
7. Copy all the required file to env/lib/python3.8/site-packages folder (Example lambda_fnction.py)
6. Cd into env/lib/python3.8/site-packages
7. Create zip of current folder with lambda_function name (zip lambda_function.zip *)
