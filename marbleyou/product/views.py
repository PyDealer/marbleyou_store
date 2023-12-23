from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.views.generic.edit import FormMixin
from django.contrib import messages

from .models import (
    Product, Stone, Category, HomePageAlbum, ProductAlbum, StoneAlbum)
from services.forms import FeedbackForm, CalculateForm, OrderForm
from services.services import Calculator, Question, Order


class QuestionFormMixin(FormView, FormMixin):
    '''Миксин формы обратной связи'''
    success_message = '''Форма успешно отправлена!
    В скором времени мы вам ответим'''
    form_class = FeedbackForm

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        question = Question(form)
        question.mail()
        messages.success(self.request, self.success_message)
        return response


class OrderFormMixin(FormView, FormMixin):
    '''Миксин формы заказа'''
    success_message = '''Спасибо за заказ!
    В скором времени мы вам ответим'''
    form_class = FeedbackForm

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        order = Order(form)
        order.mail()
        messages.success(self.request, self.success_message)
        return response


class CalculateFormMixin(FormMixin):
    '''Миксин формы калькулятора'''
    form_class = CalculateForm

    def form_valid(self, form):
        calculator = Calculator(form)
        data = [self.request.path, form.instance, ]
        if 'calculator' not in self.request.path:
            obj = self.get_object()
            data.append(obj)
            print(obj)
        process_form = calculator.main(*data)
        return render(self.request, 'product/result.html',
                      {'process_form': process_form})

    def form_invalid(self, form):
        return render(self.request, 'product/calculator.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class CategoryListView(ListView, QuestionFormMixin):
    template_name = 'product/index.html'
    model = Category
    context_object_name = 'categories'
    success_url = '/#question'
    queryset = Category.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['album'] = HomePageAlbum.objects.all()
        context['q_form'] = self.form_class()
        return context


class CategoryDetailView(CalculateFormMixin, DetailView):
    '''Страница списка изделий /product/<category_slug>/'''
    template_name = 'product/products.html'
    model = Category
    context_object_name = 'category'
    slug_url_kwarg = 'category_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        products = Product.objects.filter(category=category, is_published=True)
        context['products'] = products
        context['c_form'] = self.form_class
        return context


class ProductDetailView(DetailView):
    '''Страница изделия /product/<category_slug>/<product_slug>'''
    template_name = 'product/product_detail.html'
    model = Product
    slug_field = 'slug'
    slug_url_kwarg = 'detail_prod_slug'
    queryset = Product.objects.filter(
        is_published=True
        ).select_related('genus')
    success_message = '''Спасибо за заказ!
    В скором времени мы вам ответим'''
    c_form = CalculateForm
    o_form = OrderForm

    def get_success_url(self):
        obj = self.get_object()
        return reverse(
            'product:product_detail',
            kwargs={'category_slug': obj.category.slug,
                    'detail_prod_slug': obj.slug})

    def post(self, request, *args, **kwargs):
        if 'order' in request.POST:
            o_form = OrderForm(request.POST)
            if o_form.is_valid():
                o_form.save()
                obj = self.get_object()
                url = self.request.build_absolute_uri()
                Order(o_form, obj, url).main()
                messages.success(request, self.success_message)
                return HttpResponseRedirect(self.get_success_url())

        elif 'calc_form' in request.POST:
            c_form = CalculateForm(request.POST)
            if c_form.is_valid():
                calculator = Calculator(c_form)
                data = [self.request.path, c_form.instance, ]
                if 'calculator' not in self.request.path:
                    obj = self.get_object()
                    data.append(obj)
                    print(obj)
                process_form = calculator.main(*data)
                return render(self.request, 'product/result.html',
                              {'process_form': process_form})
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album = ProductAlbum.objects.filter(product=self.object)
        context['album'] = album
        context['stones'] = Stone.objects.filter(
            genus=self.object.genus, is_published=True)
        context['c_form'] = self.c_form
        context['o_form'] = self.o_form
        return context


class StoneDetailView(DetailView):
    '''Страница камня'''
    template_name = 'product/stone_detail.html'
    model = Stone
    slug_field = 'slug'
    slug_url_kwarg = 'stone_slug'
    context_object_name = 'stone'
    queryset = Stone.objects.filter(
        is_published=True
        )
    success_message = '''Спасибо за заказ!
    В скором времени мы вам ответим'''
    form_class = FeedbackForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album = StoneAlbum.objects.filter(stone=self.object)
        context['album'] = album
        return context


class ResultTemplateView(TemplateView):
    '''Результат расчета'''
    template_name = 'product/result.html'


class CalculatorFormView(FormView, CalculateFormMixin):
    '''Страница с формой калькулятора'''
    template_name = 'product/calculator.html'


class QuestionFormView(QuestionFormMixin):
    '''Страница с формой обратной связи'''
    template_name = 'product/question.html'
    success_url = reverse_lazy('product:question')
