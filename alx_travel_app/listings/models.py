from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin',
        GUEST = 'guest',
        HOST = 'host',

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(choices=Role.choices, default=Role.GUEST)


# Create your models here.
class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    
class Property(models.Model):
    property_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    host_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending',
        CONFIRMED = 'confirmed',
        CANCELLED = 'cancelled',

    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking {self.booking_id} for {self.property_id}"
    

class Review(models.Model):
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(min_value=1, max_value=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review {self.review_id} for {self.property_id}"
    

class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = 'credit_card',
        PAYPAL = 'paypal',
        STRIPE = 'stripe',

    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(choices=PaymentMethod.choices, default=PaymentMethod.OTHER)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_id} for {self.booking_id}"
    
    
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender_id} to {self.recipient_id}"