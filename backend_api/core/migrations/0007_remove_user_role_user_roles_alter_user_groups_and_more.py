# backend_api/core/migrations/0007_remove_user_role_user_roles_alter_user_groups_and_more.py
import django.contrib.postgres.fields
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('core', '0006_category_category_href_category_category_image_and_more'),
    ]

    operations = [

        migrations.RemoveField(
            model_name='user',
            name='role',
        ),


        migrations.AddField(
            model_name='user',
            name='roles',
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(choices=[('user', 'User'), ('admin', 'Admin')], max_length=10),
                blank=True,
                db_index=True,
                default=list,
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(
                blank=True,
                help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                related_name='user_set',
                related_query_name='user',
                to='auth.group',
                verbose_name='groups',
            ),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(
                blank=True,
                help_text='Specific permissions for this user.',
                related_name='user_set',
                related_query_name='user',
                to='auth.permission',
                verbose_name='user permissions',
            ),
        ),
    ]


# python manage.py migrate core 0007 --fake