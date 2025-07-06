"""
URL configuration for payments app.
"""
from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Payment methods
    path('methods/', views.PaymentMethodListView.as_view(), name='payment-method-list'),
    path('methods/<uuid:pk>/', views.PaymentMethodDetailView.as_view(), name='payment-method-detail'),
    
    # Transactions
    path('transactions/', views.TransactionListView.as_view(), name='transaction-list'),
    
    # Boost packages and purchases
    path('boost-packages/', views.BoostPackageListView.as_view(), name='boost-package-list'),
    path('boosts/', views.ProductBoostListView.as_view(), name='product-boost-list'),
    path('boost/purchase/', views.BoostPurchaseView.as_view(), name='boost-purchase'),
    
    # Wallet
    path('wallet/', views.WalletView.as_view(), name='wallet'),
    
    # Stripe integration
    path('create-payment-intent/', views.create_payment_intent, name='create-payment-intent'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe-webhook'),
    
    # Statistics
    path('stats/', views.payment_stats, name='payment-stats'),
]