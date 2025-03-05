1. prepare .env (rename .env.example and change environments for yours)
   If you can't crate SendGride profile, just comment line
   157. EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   in backend_api/backend_api/settings.py

In command line:

1. cd backend_api
2. pip install -r requirements.txt
3. cd ..
4. make up
5. cd backend_api
6. python manage.py makemigrations
7. python manage.py migrate
8. python manage.py createsuperuser
9. python manage.py runserver