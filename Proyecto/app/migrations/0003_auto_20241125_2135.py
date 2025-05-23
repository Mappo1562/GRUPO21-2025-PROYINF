# Generated by Django 3.2.25 on 2024-11-26 00:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_solicitud'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preenvios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='solicitud',
            name='aprobado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='solicitud',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
