from django.contrib.auth.decorators import login_required
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse

from basketapp.models import BasketItem
from mainapp.models import Product
from ordersapp.models import OrderItem


@login_required
def index(request):
    # basket_items = BasketItem.objects.filter(user=request.user)
    # basket_items = request.user.basketitem_set.filter()  # SELECT * FROM basket WHERE price_gt=2000
    # basket_items = request.user.basketitem_set.all()  # SELECT * FROM basket
    basket_items = request.user.user_basket.all()
    context = {
        'page_title': 'корзина',
        'basket_items': basket_items,
    }
    return render(request, 'basketapp/index.html', context)


@login_required
def add(request, pk):
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('auth:login'))
    # print('HTTP_REFERER', request.META.get('HTTP_REFERER'))
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(
            reverse(
                'main:product_page',
                kwargs={'pk': pk}
            )
        )

    product = get_object_or_404(Product, pk=pk)
    basket = BasketItem.objects.filter(user=request.user, product=product).first()
    # basket = request.user.basketitem_set.filter(product=pk).first()

    if not basket:
        basket = BasketItem(user=request.user, product=product)  # not in db

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
            # 'basket_cost': user.basket_cost(),
            # 'basket_total_quantity': user.basket_total_quantity(),
            # 'basket_item': basket_item,  # serialization -> drf
        })


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=BasketItem)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    print('pre_save', type(sender))
    if instance.pk:
        instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=BasketItem)
def product_quantity_update_delete(sender, instance, **kwargs):
    print('pre_delete', type(sender))
    instance.product.quantity += instance.quantity
    instance.product.save()
