from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order

# Create your views here.

class HomeView(ListView):
    model = Item
    template_name = 'home.html'


class ProductDetail(DetailView):
    model = Item
    template_name = 'product.html'


class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order
        }
        return render(self.request, 'order_summary.html', context)



def checkout(request):
    return render(request, 'checkout.html')


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, f"{item.title}'s quantity was updated")
            return redirect('order_summary')
        else:
            order.items.add(order_item)
            order.save()
            messages.success(request, f"{item.title} was added to your cart")
            return redirect('order_summary')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered=False, ordered_date=ordered_date)
        order.items.add(order_item)
        order.save()
        messages.success(request, f"{item.title} was added to your cart")
        return redirect('order_summary')


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order.items.remove(order_item)
            order.save()
            messages.success(request, f"{item.title} was removed from your cart.")
            return redirect('order_summary')
        else:
            messages.info(request, f"{item.title} was was not in your cart")
            return redirect('order_summary')
    else:
        messages.info(request, f"You do not have an active order")
        return redirect('order_summary')

def remove_single_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order.save()
            messages.success(request, f"{item.title}'s quantity was updated")
            return redirect('order_summary')
        else:
            messages.info(request, f"{item.title}'s quantity was updated")
            return redirect('order_summary')
    else:
        messages.info(request, f"You do not have an active order")
        return redirect('order_summary')
