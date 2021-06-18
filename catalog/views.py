from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order, Address
from .forms import AddressForm

import stripe


stripe.api_key = "sk_test_51J3WbnCUmH6EvAChkr4kK5eYN6s71OugkyToTSmTqQe8licaMwAKfM1SRspia9XayZzwRmCpBbCSzGK83a0wWs0I00IzopbFek"

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


class CheckoutView(View):
    def get(self, *args, **kwargs):
        # address = Address.objects.get(user=self.request.user, default=True)
        form = AddressForm()
        context = {
            'form': form,
            # 'address': address
        }
        return render(self.request, 'checkout.html', context)

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = AddressForm(self.request.POST or None)
        if form.is_valid():
            street_address = form.cleaned_data.get('street_address')
            apartment_address = form.cleaned_data.get('apartment_address')
            country = form.cleaned_data.get('country')
            zip = form.cleaned_data.get('zip')
            save_info = form.cleaned_data.get('save_info')
            use_default = form.cleaned_data.get('use_default')
            payment_option = form.cleaned_data.get('payment_option')

            address = Address(
                user=self.request.user,
                street_address=street_address,
                apartment_address=apartment_address,
                country=country,
                zip=zip
            )
            address.save()
            if save_info:
                address.default = True
                address.save()
            order.address = address
            order.save()
            
            if use_default:
                address = Address.objects.get(user=self.request.user, default=True)
                order.address = address
                order.save()

            print(form.cleaned_data)
            return redirect('checkout')
        else:
            print('form invalid')
            return redirect('checkout')


class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'payment.html')

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        costumer = stripe.Customer.create(
            email = self.request.user.email,
            description=self.request.user.username,
            source=self.request.POST['stripeToken']
        )
        amount = order.get_total()
        charge = stripe.Charge.create(
            amount=amount,
            currency="xaf",
            customer=costumer,
            description="Test payment for buteks online",
        )
        messages.success(self.request, "Payment was successful")
        return redirect('home')
    

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
