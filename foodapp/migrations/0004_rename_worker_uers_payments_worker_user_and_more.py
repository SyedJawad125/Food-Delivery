# Generated by Django 5.0.3 on 2024-03-23 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0003_alter_products_orders'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payments',
            old_name='worker_uers',
            new_name='worker_user',
        ),
        migrations.AlterField(
            model_name='products',
            name='orders',
            field=models.ManyToManyField(blank=True, null=True, related_name='kkk', to='foodapp.orders'),
        ),
    ]
