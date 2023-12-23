# Generated by Django 4.2.6 on 2023-9-30 23:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_calculationdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='stone',
            name='second_description',
            field=models.TextField(blank=True, verbose_name='Второе описание'),
        ),
        migrations.AlterField(
            model_name='calculationdata',
            name='length',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(15, message='Указывайте размеры в сантиметрах')], verbose_name='Длина'),
        ),
        migrations.AlterField(
            model_name='calculationdata',
            name='thickness',
            field=models.IntegerField(choices=[(10, '1 см'), (20, '2 см'), (30, '3 см'), (40, '4 см'), (50, '5 см')], default=30, verbose_name='Толщина'),
        ),
        migrations.AlterField(
            model_name='calculationdata',
            name='width',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(15, message='Указывайте размеры в сантиметрах')], verbose_name='Ширина'),
        ),
    ]