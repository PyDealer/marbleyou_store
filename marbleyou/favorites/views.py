from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, View
from django.template.loader import render_to_string
from django.contrib import messages

from .serializers import StoneSerializer
from product.models import Stone
from services.forms import OrderForm
from services.services import Order


def favorites_list(request):
    success_message = '''Спасибо за заказ!
    В скором времени мы вам ответим'''
    template = 'favorites/favorites_list.html'
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            messages.success(request, success_message)
            obj = ''
            url = ''
            for item in request.session['favorites']:
                obj += f'{item["type"]}\n'
            Order(form, obj, url).main()
            return redirect(request.path)
    else:
        form = OrderForm()

    context = {
        'o_form': form,
    }

    return render(request, template, context)


class FavoritesCreateView(CreateView):
    template_name = 'favorites/includes/add_favorits.html'

    def post(self, request, *args, **kwargs):
        if not request.session.get('favorites'):
            request.session['favorites'] = []
        #else:
        #    request.session['favorites'] = request.session['favorites']
        item_exist = next(
            (item for item in request.session['favorites']
             if item['type'] == request.POST.get('type') and str(item['stone_id']) == request.POST.get('stone_id')), False)
        data = {
            'type': request.POST.get('type'),
            'stone_id': kwargs['id'],
            'url': self.request.POST.get('url_from')
        }

        status = False
        if not item_exist:
            status = True
            request.session['favorites'].append(data)
            request.session.modified = True
        else:
            request.session['favorites'].remove(data)
            request.session.modified = True

        favorites = request.session.get('favorites', [])
        stone_ids = [item['stone_id'] for item in favorites]
        stones = Stone.objects.filter(id__in=stone_ids)
        serializer = StoneSerializer(stones, many=True)
        serialized_data = serializer.data
        favorites_list_html = render_to_string('includes/modal_list.html', {'favorites_list_modal': serialized_data}, request=request)
        #request.session.flush()

        return JsonResponse({'count': len(request.session['favorites']),
                             'data': request.session['favorites'],
                             'status': status,
                             'modal_list': favorites_list_html})


class FavoritesClearView(View):
    def post(self, request, *args, **kwargs):
        stone_ids = [
            item['stone_id'] for item in request.session.get('favorites', [])]
        print(stone_ids)
        del request.session['favorites']
        request.session.modified = True
        return JsonResponse(
            {'modal_list': '<div class="container" id="modal_list"></div>',
             'stone_ids': stone_ids})
