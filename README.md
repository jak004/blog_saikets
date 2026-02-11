# Porres Blogging Site (Django + SQLite)

## Quick start
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows
# or: cp .env.example .env

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:
- Site: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/admin

## Guest comments + moderation
Guests can comment with **name + email**, but comments are hidden until approved:
Admin → Comments → select → **Approve comments**
