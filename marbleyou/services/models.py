from django.db import models
from django.core.validators import MinValueValidator

from phonenumber_field.modelfields import PhoneNumberField

ERR_MSG = 'Указывайте размеры в сантиметрах'


class WorkPrice(models.Model):
    cut = models.IntegerField('Рез камня', default=700)
    edge = models.IntegerField('Кромка', default=1300)
    average = models.IntegerField('Средняя стоимость материала', default=13000)
    hob = models.IntegerField('Вырез под плиту', default=3200)
    sink = models.IntegerField('Вырез под раковину', default=4000)
    tap = models.IntegerField('Отверстие под кран', default=1500)
    dropper = models.IntegerField('Капельник', default=400)

    class Meta:
        verbose_name = 'цена производства'
        verbose_name_plural = 'Цены на производство'


class CalculationRequest(models.Model):
    status = models.BooleanField('Обработана', default=False)
    name = models.CharField('Имя', max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = PhoneNumberField('Телефон', region='RU', null=True, blank=True)
    product = models.CharField(
        'Изделие', max_length=256, null=True, blank=True,
        default='Изделие не указано')
    length = models.IntegerField(
        'Длина',
        validators=[MinValueValidator(
            15, message=ERR_MSG)])
    width = models.IntegerField(
        'Ширина',
        validators=[MinValueValidator(
            15, message=ERR_MSG)])
    THICKNESS_CHOICES = (
        (10, '1 см'),
        (20, '2 см'),
        (30, '3 см'),
        (40, '4 см'),
        (50, '5 см'),
    )
    thickness = models.IntegerField(
        'Толщина', choices=THICKNESS_CHOICES, default=30)
    cut = models.IntegerField('Рез камня', null=True, blank=True)
    edge = models.IntegerField('Полировка кромки', null=True, blank=True)
    array = models.IntegerField('Площадь материала', null=True, blank=True)
    hob = models.BooleanField('Вырез под варочную панель', default=False)
    sink = models.BooleanField('Вырез под раковину', default=False)
    tap = models.BooleanField('Отверстие под кран', default=False)
    riser_array = models.IntegerField(
        'Площадь материала подступенка', null=True, blank=True)
    dropper = models.IntegerField('Капельник', null=True, blank=True)
    message = models.TextField('Сообщение', null=True, blank=True)
    final_price_production = models.IntegerField(
        'Общая стоимость производства', null=True, blank=True)
    final_price = models.IntegerField(
        'Итоговая стоимость', null=True, blank=True)
    general_info = models.TextField(
        'Общая информация', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время')

    def __str__(self):
        return f'Заявка №{self.id}. {self.name or ""} {self.email or ""}'

    class Meta:
        verbose_name = 'расчет'
        verbose_name_plural = 'Заявка на расчет'


class Feedback(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    message = models.TextField(verbose_name='Ваш вопрос')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время')
    status = models.BooleanField('Обработана', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'Форма обратной связи'


class Order(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    message = models.TextField(
        verbose_name='Комментарий к заказу', blank=True)
    STATUS_CHOICES = [
        ('Открытый', 'Открытый'),
        ('В работе', 'В работе'),
        ('Закрытый', 'Закрытый'),
    ]
    status = models.CharField(
        'Статус', max_length=20, choices=STATUS_CHOICES, default="Открытый")
    composition = models.TextField(verbose_name='Состав заказа', blank=True)
    addition = models.TextField(verbose_name='Дополнение к заказу', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'
