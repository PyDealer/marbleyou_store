from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field, HTML

from product.models import Category, Genus
from .models import Feedback, CalculationRequest, Order


class FeedbackForm(forms.ModelForm):
    '''Форма обратной связи'''
    title = 'Обратная связь'
    message = forms.CharField(
        label='Ваш вопрос',
        widget=forms.Textarea(attrs={'rows': 4, 'autocomplete': 0}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            self.helper.add_input(
                Submit('question', 'Отправить',
                       css_class='btn-myform')))

    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']


class OrderForm(forms.ModelForm):
    '''Форма заказа'''
    title = 'Заказ'
    message = forms.CharField(
        label='Оставьте комментарий',
        widget=forms.Textarea(attrs={'rows': 4, 'autocomplete': 0}),
        required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            self.helper.add_input(
                Submit('order', 'Заказать',
                       css_class='btn-myform')))

    class Meta:
        model = Order
        fields = ['name', 'email', 'message']


class CalculateForm(forms.ModelForm):
    '''Калькулятор стоимости изделия'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('length', css_class='col-md-4'),
                Column('width', css_class='col-md-4'),
                Column('thickness', css_class='col-md-4'),
                css_class='form-row'
            ),
            HTML('''
                 {% load crispy_forms_tags %}
                 {% if 'calculator' in request.path %}
                 <div class="row">
                    <div class="col-md-6">
                        {{ form.category|as_crispy_field }}
                    </div>
                    <div class="col-md-6">
                        {{ form.genus|as_crispy_field }}
                    </div>
                </div>
                 {% endif%}
                 '''),
            HTML('''
                 {% load crispy_forms_tags %}
                 {% if 'tabletop' in request.path or 'calculator' in request.path %}
                 <p>Выберите атрибуты, которые планируете устанавливать:</p>
                 <div class="row">
                    <div class="col-md-4">
                        {{ form.hob|as_crispy_field }}
                    </div>
                    <div class="col-md-4">
                        {{ form.sink|as_crispy_field }}
                    </div>
                    <div class="col-md-4">
                        {{ form.tap|as_crispy_field }}
                    </div>
                </div>
                 {% endif%}
                 '''),
            Row(
                Column('email', css_class='col-md-6'),
                Column('phone', css_class='col-md-6'),
                css_class='form-row'
            ),
            Field('name'),
            Field('message'),
        )
        self.helper.add_input(Submit(
            'calc_form', 'Посчитать',
            css_class='btn-myform'))

    title = 'Калькулятор стоимости'
    description = 'Размеры указывайте в сантиметрах'
    category = forms.ModelChoiceField(
        label='Изделие',
        queryset=Category.objects.all(),
        empty_label='Выберите изделие',
        required=False,
    )
    genus = forms.ModelChoiceField(
        label='Камень',
        queryset=Genus.objects.all(),
        empty_label='Выберите камень',
        required=False,
    )

    class Meta:
        model = CalculationRequest
        fields = ['length', 'width', 'thickness', 'category', 'genus', 'hob',
                  'sink', 'tap', 'name', 'phone', 'email', 'message']

        widgets = {
            'message': forms.Textarea(attrs={'rows': 2, 'autocomplete': 0}),
        }
