from django.db import migrations, models

def migrate_roles_to_role(apps, schema_editor):
    User = apps.get_model('core', 'User')
    for user in User.objects.all():
        # Переносимо перше значення з масиву roles або встановлюємо 'customer'
        if hasattr(user, 'roles') and user.roles and user.roles[0]:
            user.role = user.roles[0]
        else:
            user.role = 'customer'
        user.save()

def reverse_migrate_roles_to_role(apps, schema_editor):
    User = apps.get_model('core', 'User')
    for user in User.objects.all():
        user.roles = [user.role] if user.role else []
        user.save()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0006_category_category_href_category_category_image_and_more'),
    ]
    operations = [
        # Знімаємо обмеження NOT NULL для roles
        migrations.RunSQL(
            'ALTER TABLE core_user ALTER COLUMN roles DROP NOT NULL;',
            'ALTER TABLE core_user ALTER COLUMN roles SET NOT NULL;'
        ),
        # Додаємо поле role
        migrations.AddField(
            model_name='User',
            name='role',
            field=models.CharField(
                max_length=10,
                choices=[('customer', 'Customer'), ('vendor', 'Vendor'), ('admin', 'Admin')],
                default='customer',
                db_index=True
            ),
        ),
        # Переносимо дані
        migrations.RunPython(migrate_roles_to_role, reverse_migrate_roles_to_role),
        # Видаляємо стовпець roles
        migrations.RunSQL(
            'ALTER TABLE core_user DROP COLUMN roles;',
            'ALTER TABLE core_user ADD COLUMN roles character varying(10)[] NOT NULL DEFAULT \'{}\';'
        ),
    ]