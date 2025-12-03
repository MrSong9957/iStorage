# Generated minimal migration to add Category model
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('items', '0002_remove_room_user_alter_storagecell_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='分类名称')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to=settings.AUTH_USER_MODEL, verbose_name='所属用户')),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
                'unique_together': {('user', 'name')},
            },
        ),
    ]
