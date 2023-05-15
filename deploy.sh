# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py makemigrations --no-input
python manage.py migrate --no-input