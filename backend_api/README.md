1. prepare .env (rename .env.example and change environments for yours)
   If you can't crate SendGride profile, just comment line
   157. EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   in backend_api/backend_api/settings.py

In command line:

1. make up :
   check your environ, if not exist, create and activate
   install all packages from requirements.txt
   create postgresql and redis docker container

2. make migrate :
   migrate all changes in db structure

3. make super :
   create superuser in db

4. make run :
   start django server

5. make down :
   stop and delete docker containers