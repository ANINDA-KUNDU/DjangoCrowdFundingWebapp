from django.urls import path
from . import views

urlpatterns = [
    path('fund', views.fund, name = "fund"),
    path('checkout/<int:pk>', views.CheckoutViewSession, name = "checkout"),
    path('success-page/<int:pk>', views.success_page, name = "success_page"),
    path('fail-page', views.fail_page, name = "fail_page"),
    path('stripe-webhook', views.stripe_webhook, name = 'stripe_webhook'),
]