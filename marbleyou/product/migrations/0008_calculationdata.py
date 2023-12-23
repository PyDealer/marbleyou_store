# Generated by Django 4.2.6 on 2023-7-27 16:04

import django.core.validators
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_question_rename_product_stonealbum_stone'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalculationData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False, verbose_name='Обработана')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Имя')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region='RU', verbose_name='Телефон')),
                ('product', models.CharField(blank=True, default='Изделие не указано', max_length=256, null=True, verbose_name='Изделие')),
                ('length', models.IntegerField(validators=[django.core.validators.MinValueValidator(200, message='Указывайте размеры в миллиметрах')], verbose_name='Длина')),
                ('width', models.IntegerField(validators=[django.core.validators.MinValueValidator(200, message='Указывайте размеры в миллиметрах')], verbose_name='Ширина')),
                ('thickness', models.IntegerField(choices=[(10, '10 мм'), (20, '20 мм'), (30, '30 мм'), (40, '40 мм'), (50, '50 мм')], default=30, verbose_name='Толщина')),
                ('cut', models.IntegerField(blank=True, null=True, verbose_name='Рез камня')),
                ('edge', models.IntegerField(blank=True, null=True, verbose_name='Полировка кромки')),
                ('array', models.IntegerField(blank=True, null=True, verbose_name='Площадь материала')),
                ('hob', models.BooleanField(default=False, verbose_name='Вырез под варочную панель')),
                ('sink', models.BooleanField(default=False, verbose_name='Вырез под раковину')),
                ('tap', models.BooleanField(default=False, verbose_name='Отверстие под кран')),
                ('riser_array', models.IntegerField(blank=True, null=True, verbose_name='Площадь материала подступенка')),
                ('dropper', models.IntegerField(blank=True, null=True, verbose_name='Капельник')),
                ('message', models.TextField(blank=True, null=True, verbose_name='Сообщение')),
                ('final_price_production', models.IntegerField(blank=True, null=True, verbose_name='Общая стоимость производства')),
                ('final_price', models.IntegerField(blank=True, null=True, verbose_name='Итоговая стоимость')),
                ('general_info', models.TextField(blank=True, null=True, verbose_name='Общая информация')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время')),
            ],
            options={
                'verbose_name': 'расчет',
                'verbose_name_plural': 'Заявка на расчет',
            },
        ),
    ]
