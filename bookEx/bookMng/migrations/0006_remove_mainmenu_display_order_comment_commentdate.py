# Generated by Django 5.0.4 on 2024-06-07 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookMng', '0005_mainmenu_display_order'),
    ]

    operations = [
        #migrations.RemoveField(
        #    model_name='mainmenu',
         #   name='display_order',
        #),
        migrations.AddField(
            model_name='comment',
            name='commentdate',
            field=models.DateField(auto_now=True),
        ),
    ]
