from product.models import Stone


def favorites(request):
    numeric_ids = []
    favorites = request.session.get('favorites', [])
    numeric_ids = [
        item['stone_id'] for item in favorites if isinstance(
            item['stone_id'], int)]

    return {
        'favorites_ids': numeric_ids,
        'favorites_list_modal': Stone.objects.filter(id__in=numeric_ids),
        'count': len(request.session.get('favorites', [])),
    }
