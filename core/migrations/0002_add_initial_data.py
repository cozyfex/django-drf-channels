from django.db import migrations


def create_initial_permission_data(apps, schema_editor):
    Permission = apps.get_model('core', 'Permission')

    permission = Permission.objects.create(
        code='SUPER_ADMIN',
    )
    permission.save()


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_permission_data),
    ]
