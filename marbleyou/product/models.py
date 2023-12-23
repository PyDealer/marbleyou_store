from django.db import models


class Genus(models.Model):
    name = models.CharField('Вид камня (например: гранит)', max_length=256)
    description = models.TextField('Описание', blank=True)
    slug = models.SlugField(
        'Идентификатор',
        max_length=64,
        unique=True,
        help_text=('Идентификатор страницы для URL; разрешены символы '
                   'латиницы, цифры, дефис и подчёркивание.')
    )

    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    class Meta:
        verbose_name = 'вид камня'
        verbose_name_plural = 'Виды камня'

    def __str__(self):
        return self.name


class Stone(models.Model):
    name = models.CharField('Название', max_length=256)
    description = models.TextField('Описание', blank=True)
    second_description = models.TextField('Второе описание', blank=True)
    image = models.ImageField('Изображение', upload_to='images/stone',
                              blank=True)
    length = models.IntegerField('Длина мм', blank=True, null=True)
    width = models.IntegerField('Ширина мм', blank=True, null=True)
    thickness = models.IntegerField('Толщина мм', blank=True, null=True)
    slug = models.SlugField(
        'Идентификатор',
        max_length=64,
        unique=True,
        help_text=('Идентификатор страницы для URL; разрешены символы '
                   'латиницы, цифры, дефис и подчёркивание.')
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True)

    genus = models.ForeignKey(
        Genus,
        on_delete=models.SET_NULL,
        null=True,
        related_name='genus',
        verbose_name='Вид камня'
    )

    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    class Meta:
        verbose_name = 'камень'
        verbose_name_plural = 'Камень'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        'Название категории (пример: столешницы, лестницы)',
        max_length=256)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Изображение', upload_to='images/category',
                              blank=True)
    slug = models.SlugField(
        'Идентификатор',
        max_length=64,
        unique=True,
        help_text=('Идентификатор страницы для URL; разрешены символы '
                   'латиницы, цифры, дефис и подчёркивание.')
    )
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    class Meta:
        verbose_name = 'категория изделий'
        verbose_name_plural = 'Категории изделий'

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(
        'Наименование изделия (пример: столешницы из сланца)',
        max_length=256)
    description = models.TextField('Описание', blank=True)
    second_description = models.TextField('Второе описание', blank=True)
    image = models.ImageField('Изображение', upload_to='images/product',
                              blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True)
    slug = models.SlugField(
        'Идентификатор',
        max_length=64,
        unique=True,
        help_text=('Идентификатор страницы для URL; разрешены символы '
                   'латиницы, цифры, дефис и подчёркивание.')
    )
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category',
        verbose_name='Категория изделия'
    )

    genus = models.ForeignKey(
        Genus,
        on_delete=models.SET_NULL,
        null=True,
        related_name='product_genus',
        verbose_name='Вид камня'
    )

    class Meta:
        verbose_name = 'изделие'
        verbose_name_plural = 'Изделия'

    def __str__(self):
        return self.title


class ProductAlbum(models.Model):
    product = models.ForeignKey(
        Product, blank=True, related_name='product_album',
        on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/product/album', blank=True)

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'Альбом изделий в карусель'


class StoneAlbum(models.Model):
    stone = models.ForeignKey(
        Stone, blank=True, related_name='stone_album',
        on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/stone/album', blank=True)

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'Альбом камня'


class HomePage(models.Model):
    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'Альбом карусели на главной'


class HomePageAlbum(models.Model):
    homepage = models.ForeignKey(
        HomePage, blank=True, related_name='homepage_album',
        on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/homepage/album', blank=True)

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'Альбом главной'

