from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse

from basketapp.models import BasketItem
from mainapp.models import Product


@login_required
def index(request):
    basket_items = request.user.user_basket.all()
    context = {
        'page_title': 'корзина',
        'basket_items': basket_items,
    }
    return render(request, 'basketapp/index.html', context)


@login_required
def add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(
            reverse(
                'main:product_page',
                kwargs={'pk': pk}
            )
        )

    product = get_object_or_404(Product, pk=pk)
    basket = BasketItem.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = BasketItem(user=request.user, product=product)

    basket.quantity += 1
    basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete(request, pk):
    get_object_or_404(BasketItem, pk=pk).delete()
    return HttpResponseRedirect(reverse('basket:index'))


def change(request, pk, quantity):
    if request.is_ajax():
        basket_item = BasketItem.objects.filter(pk=pk).first()
        if quantity == 0:
            basket_item.delete()
        else:
            # quantity validation
            basket_item.quantity = quantity
            basket_item.save()

        context = {
            'basket_items': request.user.user_basket.all(),
        }

        basket_items = loader.render_to_string(
            'basketapp/inc/inc__basket_items.html',
            context=context,
            request=request,  # csrf token update
        )

        return JsonResponse({
            'basket_items': basket_items,
        })
