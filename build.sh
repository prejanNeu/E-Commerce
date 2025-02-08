set -o errexit 

pip install -r requirements.txt 

python manage.py collectctstatic --no-input

python manage.py migrate