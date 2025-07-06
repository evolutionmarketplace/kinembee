"""
Views for payments.
"""
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import stripe

from .models import PaymentMethod, Transaction, BoostPackage, ProductBoost, Wallet
from .serializers import (
    PaymentMethodSerializer, TransactionSerializer, BoostPackageSerializer,
    ProductBoostSerializer, WalletSerializer, BoostPurchaseSerializer
)
from apps.core.pagination import CustomPageNumberPagination

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentMethodListView(generics.ListCreateAPIView):
    """
    List and create payment methods.
    """
    serializer_class = PaymentMethodSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PaymentMethod.objects.filter(user=self.request.user, is_active=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaymentMethodDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a payment method.
    """
    serializer_class = PaymentMethodSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PaymentMethod.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class TransactionListView(generics.ListAPIView):
    """
    List user's transactions.
    """
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        
        # Filter by transaction type
        transaction_type = self.request.query_params.get('type')
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-created_at')


class BoostPackageListView(generics.ListAPIView):
    """
    List available boost packages.
    """
    serializer_class = BoostPackageSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return BoostPackage.objects.filter(is_active=True).order_by('sort_order', 'price')


class ProductBoostListView(generics.ListAPIView):
    """
    List user's product boosts.
    """
    serializer_class = ProductBoostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProductBoost.objects.filter(user=self.request.user).order_by('-created_at')


class WalletView(generics.RetrieveUpdateAPIView):
    """
    Get and update wallet information.
    """
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        wallet, created = Wallet.objects.get_or_create(user=self.request.user)
        return wallet


class BoostPurchaseView(APIView):
    """
    Purchase a boost for a product.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = BoostPurchaseSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        try:
            # Get objects
            from apps.products.models import Product
            product = Product.objects.get(id=serializer.validated_data['product_id'])
            package = BoostPackage.objects.get(id=serializer.validated_data['package_id'])
            payment_method = PaymentMethod.objects.get(id=serializer.validated_data['payment_method_id'])
            
            # Create Stripe payment intent
            payment_intent = stripe.PaymentIntent.create(
                amount=int(package.price * 100),  # Convert to cents
                currency='usd',
                payment_method=payment_method.stripe_payment_method_id,
                confirm=True,
                return_url=f"{settings.FRONTEND_URL}/boost-success",
                metadata={
                    'product_id': str(product.id),
                    'package_id': str(package.id),
                    'user_id': str(request.user.id)
                }
            )
            
            # Create transaction
            transaction = Transaction.objects.create(
                user=request.user,
                transaction_type='boost_payment',
                amount=package.price,
                fee_amount=package.price * 0.03,  # 3% platform fee
                payment_method=payment_method,
                product=product,
                stripe_payment_intent_id=payment_intent.id,
                description=f"Boost purchase for {product.title}",
                status='completed' if payment_intent.status == 'succeeded' else 'pending'
            )
            
            if payment_intent.status == 'succeeded':
                # Create product boost
                starts_at = timezone.now()
                expires_at = starts_at + timedelta(days=package.duration_days)
                
                ProductBoost.objects.create(
                    product=product,
                    user=request.user,
                    package=package,
                    transaction=transaction,
                    starts_at=starts_at,
                    expires_at=expires_at
                )
                
                # Update product boost status
                product.is_boosted = True
                product.boost_expires_at = expires_at
                product.save()
                
                return Response({
                    'success': True,
                    'message': 'Boost purchased successfully',
                    'transaction_id': transaction.transaction_id
                })
            else:
                return Response({
                    'success': False,
                    'message': 'Payment failed',
                    'payment_intent_status': payment_intent.status
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except stripe.error.StripeError as e:
            return Response({
                'success': False,
                'message': f'Payment error: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_payment_intent(request):
    """
    Create a Stripe payment intent for boost purchase.
    """
    try:
        package_id = request.data.get('package_id')
        package = BoostPackage.objects.get(id=package_id, is_active=True)
        
        payment_intent = stripe.PaymentIntent.create(
            amount=int(package.price * 100),
            currency='usd',
            metadata={
                'package_id': str(package.id),
                'user_id': str(request.user.id)
            }
        )
        
        return Response({
            'client_secret': payment_intent.client_secret,
            'amount': package.price
        })
        
    except BoostPackage.DoesNotExist:
        return Response({'error': 'Package not found'}, status=status.HTTP_404_NOT_FOUND)
    except stripe.error.StripeError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def stripe_webhook(request):
    """
    Handle Stripe webhooks.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return Response({'error': 'Invalid payload'}, status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError:
        return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        # Handle successful payment
        handle_successful_payment(payment_intent)
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        # Handle failed payment
        handle_failed_payment(payment_intent)
    
    return Response({'status': 'success'})


def handle_successful_payment(payment_intent):
    """Handle successful payment from webhook."""
    try:
        transaction = Transaction.objects.get(
            stripe_payment_intent_id=payment_intent['id']
        )
        transaction.status = 'completed'
        transaction.processed_at = timezone.now()
        transaction.save()
    except Transaction.DoesNotExist:
        pass


def handle_failed_payment(payment_intent):
    """Handle failed payment from webhook."""
    try:
        transaction = Transaction.objects.get(
            stripe_payment_intent_id=payment_intent['id']
        )
        transaction.status = 'failed'
        transaction.failure_reason = payment_intent.get('last_payment_error', {}).get('message', '')
        transaction.save()
    except Transaction.DoesNotExist:
        pass


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def payment_stats(request):
    """
    Get payment statistics for the user.
    """
    user = request.user
    
    stats = {
        'total_spent': Transaction.objects.filter(
            user=user,
            transaction_type='boost_payment',
            status='completed'
        ).aggregate(total=models.Sum('amount'))['total'] or 0,
        
        'active_boosts': ProductBoost.objects.filter(
            user=user,
            is_active=True,
            expires_at__gt=timezone.now()
        ).count(),
        
        'total_transactions': Transaction.objects.filter(user=user).count(),
        
        'pending_transactions': Transaction.objects.filter(
            user=user,
            status='pending'
        ).count(),
    }
    
    return Response(stats)