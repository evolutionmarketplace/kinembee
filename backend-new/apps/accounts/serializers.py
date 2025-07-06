"""
Serializers for user accounts and authentication.
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, UserProfile, UserPreferences
from apps.core.utils import mask_email, mask_phone


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    terms_accepted = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone_number', 'terms_accepted'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        
        if not attrs.get('terms_accepted'):
            raise serializers.ValidationError("You must accept the terms and conditions.")
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        validated_data.pop('terms_accepted')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            
            if user.is_banned:
                raise serializers.ValidationError('User account is banned.')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include email and password.')


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile.
    """
    full_name = serializers.ReadOnlyField()
    verification_level = serializers.ReadOnlyField(source='profile.verification_level')
    seller_rating = serializers.ReadOnlyField(source='profile.seller_rating')
    total_sales = serializers.ReadOnlyField(source='profile.total_sales')
    total_reviews = serializers.ReadOnlyField(source='profile.total_reviews')
    is_active_user = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone_number', 'avatar', 'bio', 'is_verified', 'is_business',
            'business_name', 'verification_level', 'seller_rating', 'total_sales',
            'total_reviews', 'is_active_user', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'email', 'is_verified', 'date_joined', 'last_login']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    """
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number', 'avatar', 'bio',
            'business_name'
        ]

    def validate_phone_number(self, value):
        if value and User.objects.filter(phone_number=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value


class PublicUserSerializer(serializers.ModelSerializer):
    """
    Serializer for public user information (for listings, reviews, etc.).
    """
    full_name = serializers.ReadOnlyField()
    seller_rating = serializers.ReadOnlyField(source='profile.seller_rating')
    total_sales = serializers.ReadOnlyField(source='profile.total_sales')
    total_reviews = serializers.ReadOnlyField(source='profile.total_reviews')
    response_rate = serializers.ReadOnlyField(source='profile.response_rate')
    verification_level = serializers.ReadOnlyField(source='profile.verification_level')
    masked_email = serializers.SerializerMethodField()
    masked_phone = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'full_name', 'avatar', 'bio', 'is_verified',
            'is_business', 'business_name', 'seller_rating', 'total_sales',
            'total_reviews', 'response_rate', 'verification_level',
            'masked_email', 'masked_phone', 'date_joined'
        ]

    def get_masked_email(self, obj):
        return mask_email(obj.email) if obj.email else None

    def get_masked_phone(self, obj):
        return mask_phone(obj.phone_number) if obj.phone_number else None


class UserPreferencesSerializer(serializers.ModelSerializer):
    """
    Serializer for user preferences.
    """
    class Meta:
        model = UserPreferences
        exclude = ['id', 'user', 'created_at', 'updated_at']


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for password change.
    """
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class EmailVerificationSerializer(serializers.Serializer):
    """
    Serializer for email verification.
    """
    token = serializers.CharField()

    def validate_token(self, value):
        from .models import EmailVerification
        
        try:
            verification = EmailVerification.objects.get(token=value)
            if not verification.is_valid:
                raise serializers.ValidationError("Invalid or expired token.")
            self.verification = verification
            return value
        except EmailVerification.DoesNotExist:
            raise serializers.ValidationError("Invalid token.")


class PhoneVerificationSerializer(serializers.Serializer):
    """
    Serializer for phone verification.
    """
    phone_number = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        from .models import PhoneVerification
        
        try:
            verification = PhoneVerification.objects.get(
                phone_number=attrs['phone_number'],
                code=attrs['code']
            )
            if not verification.is_valid:
                raise serializers.ValidationError("Invalid or expired code.")
            self.verification = verification
            return attrs
        except PhoneVerification.DoesNotExist:
            raise serializers.ValidationError("Invalid verification code.")