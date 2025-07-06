"""
Utility functions for Evolution Digital Market.
"""
import os
import uuid
import hashlib
from PIL import Image
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils.text import slugify
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
import requests

logger = logging.getLogger(__name__)


def generate_unique_filename(filename):
    """
    Generate a unique filename while preserving the extension.
    """
    name, ext = os.path.splitext(filename)
    unique_name = f"{uuid.uuid4().hex}{ext}"
    return unique_name


def compress_image(image, quality=85, max_width=1200, max_height=1200):
    """
    Compress and resize an image.
    """
    try:
        img = Image.open(image)
        
        # Convert to RGB if necessary
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        
        # Resize if necessary
        if img.width > max_width or img.height > max_height:
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        # Save compressed image
        from io import BytesIO
        output = BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        
        return ContentFile(output.read())
    except Exception as e:
        logger.error(f"Error compressing image: {e}")
        return image


def create_thumbnail(image, size=(300, 300)):
    """
    Create a thumbnail from an image.
    """
    try:
        img = Image.open(image)
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        from io import BytesIO
        output = BytesIO()
        img.save(output, format='JPEG', quality=90)
        output.seek(0)
        
        return ContentFile(output.read())
    except Exception as e:
        logger.error(f"Error creating thumbnail: {e}")
        return None


def send_notification_email(user, subject, template_name, context):
    """
    Send notification email to user using Resend.
    """
    try:
        context['user'] = user
        html_message = render_to_string(f'emails/{template_name}.html', context)
        plain_message = strip_tags(html_message)
        
        # Use Django's built-in email backend (configured for Resend)
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Email sent to {user.email}: {subject}")
    except Exception as e:
        logger.error(f"Error sending email to {user.email}: {e}")


def send_resend_email(to_email, subject, html_content, text_content=None):
    """
    Send email using Resend API directly.
    """
    try:
        import requests
        
        url = "https://api.resend.com/emails"
        
        payload = {
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [to_email],
            "subject": subject,
            "html": html_content,
        }
        
        if text_content:
            payload["text"] = text_content
        
        headers = {
            "Authorization": f"Bearer {settings.RESEND_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            logger.info(f"Resend email sent successfully to {to_email}")
            return True
        else:
            logger.error(f"Resend API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending Resend email: {e}")
        return False


def send_welcome_email(user):
    """
    Send welcome email to new user.
    """
    subject = "Welcome to Evolution Digital Market!"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Welcome to Evolution Market</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .button {{ display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 Welcome to Evolution Market!</h1>
                <p>Your journey in the digital marketplace begins now</p>
            </div>
            <div class="content">
                <h2>Hi {user.first_name or user.username}!</h2>
                <p>Thank you for joining Evolution Digital Market - the premier peer-to-peer marketplace for everything digital and beyond.</p>
                
                <h3>🚀 What you can do now:</h3>
                <ul>
                    <li>✅ Browse thousands of products and services</li>
                    <li>✅ List your own items for sale</li>
                    <li>✅ Connect with buyers and sellers</li>
                    <li>✅ Secure payments and transactions</li>
                    <li>✅ Real-time chat with other users</li>
                </ul>
                
                <a href="{settings.FRONTEND_URL}" class="button">Start Exploring</a>
                
                <h3>💡 Pro Tips:</h3>
                <ul>
                    <li>Complete your profile to build trust</li>
                    <li>Add clear photos to your listings</li>
                    <li>Respond quickly to messages</li>
                    <li>Use our boost feature for better visibility</li>
                </ul>
                
                <p>If you have any questions, our support team is here to help!</p>
            </div>
            <div class="footer">
                <p>Happy selling! 🛍️<br>
                The Evolution Market Team</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Welcome to Evolution Digital Market!
    
    Hi {user.first_name or user.username}!
    
    Thank you for joining Evolution Digital Market - the premier peer-to-peer marketplace.
    
    What you can do now:
    - Browse thousands of products and services
    - List your own items for sale
    - Connect with buyers and sellers
    - Secure payments and transactions
    - Real-time chat with other users
    
    Visit: {settings.FRONTEND_URL}
    
    Happy selling!
    The Evolution Market Team
    """
    
    return send_resend_email(user.email, subject, html_content, text_content)


def send_verification_email(user, verification_url):
    """
    Send email verification email.
    """
    subject = "Verify your Evolution Market account"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Verify Your Account</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .button {{ display: inline-block; background: #28a745; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔐 Verify Your Account</h1>
                <p>Just one more step to get started!</p>
            </div>
            <div class="content">
                <h2>Hi {user.first_name or user.username}!</h2>
                <p>Please verify your email address to complete your Evolution Market registration.</p>
                
                <a href="{verification_url}" class="button">Verify Email Address</a>
                
                <p>Or copy and paste this link in your browser:</p>
                <p style="word-break: break-all; background: #e9ecef; padding: 10px; border-radius: 5px;">{verification_url}</p>
                
                <p><strong>This link will expire in 24 hours.</strong></p>
                
                <p>If you didn't create an account with us, please ignore this email.</p>
            </div>
            <div class="footer">
                <p>Thanks!<br>
                The Evolution Market Team</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Verify Your Evolution Market Account
    
    Hi {user.first_name or user.username}!
    
    Please verify your email address to complete your registration.
    
    Click here to verify: {verification_url}
    
    This link will expire in 24 hours.
    
    If you didn't create an account with us, please ignore this email.
    
    Thanks!
    The Evolution Market Team
    """
    
    return send_resend_email(user.email, subject, html_content, text_content)


def generate_slug(text, max_length=50):
    """
    Generate a URL-friendly slug from text.
    """
    slug = slugify(text)
    if len(slug) > max_length:
        slug = slug[:max_length].rstrip('-')
    return slug


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two coordinates using Haversine formula.
    Returns distance in kilometers.
    """
    from math import radians, cos, sin, asin, sqrt
    
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    
    return c * r


def generate_verification_token():
    """
    Generate a secure verification token.
    """
    return hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()


def mask_email(email):
    """
    Mask email address for privacy.
    """
    username, domain = email.split('@')
    if len(username) <= 2:
        masked_username = username[0] + '*'
    else:
        masked_username = username[0] + '*' * (len(username) - 2) + username[-1]
    return f"{masked_username}@{domain}"


def mask_phone(phone):
    """
    Mask phone number for privacy.
    """
    if len(phone) <= 4:
        return '*' * len(phone)
    return phone[:2] + '*' * (len(phone) - 4) + phone[-2:]


class FileUploadHandler:
    """
    Handle file uploads with validation and processing.
    """
    
    ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']
    ALLOWED_DOCUMENT_EXTENSIONS = ['.pdf', '.doc', '.docx']
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @classmethod
    def validate_image(cls, file):
        """
        Validate uploaded image file.
        """
        # Check file size
        if file.size > cls.MAX_FILE_SIZE:
            raise ValueError("File size too large. Maximum size is 10MB.")
        
        # Check file extension
        name, ext = os.path.splitext(file.name.lower())
        if ext not in cls.ALLOWED_IMAGE_EXTENSIONS:
            raise ValueError(f"Invalid file type. Allowed types: {', '.join(cls.ALLOWED_IMAGE_EXTENSIONS)}")
        
        # Validate image content
        try:
            img = Image.open(file)
            img.verify()
        except Exception:
            raise ValueError("Invalid image file.")
        
        return True
    
    @classmethod
    def process_product_image(cls, image_file, product_id):
        """
        Process and save product image.
        """
        cls.validate_image(image_file)
        
        # Generate unique filename
        name, ext = os.path.splitext(image_file.name)
        filename = f"products/{product_id}/{uuid.uuid4().hex}{ext}"
        
        # Compress image
        compressed_image = compress_image(image_file)
        
        # Save to storage
        path = default_storage.save(filename, compressed_image)
        
        # Create thumbnail
        thumbnail = create_thumbnail(compressed_image)
        if thumbnail:
            thumb_filename = f"products/{product_id}/thumbnails/{uuid.uuid4().hex}{ext}"
            thumb_path = default_storage.save(thumb_filename, thumbnail)
        else:
            thumb_path = path
        
        return {
            'original': path,
            'thumbnail': thumb_path,
            'url': default_storage.url(path),
            'thumbnail_url': default_storage.url(thumb_path)
        }