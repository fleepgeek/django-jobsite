# Generated by Django 2.0.4 on 2018-04-25 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_auto_20180425_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='industry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Industry'),
        ),
    ]