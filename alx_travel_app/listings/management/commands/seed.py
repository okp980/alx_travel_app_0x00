import random
from decimal import Decimal
from datetime import datetime, timedelta, date

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import lorem_ipsum
from listings.models import User, Property, Booking, Review, Payment, Message, Listing


class Command(BaseCommand):
    help = 'Seed the database with sample data for the travel app'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            self.clear_data()

        self.stdout.write('Starting to seed database...')
        
        # Create users first (required for other models)
        users = self.seed_users()
        
        # Create properties and listings
        properties = self.seed_properties(users)
        listings = self.seed_listings()
        
        # Create bookings
        bookings = self.seed_bookings(properties, users)
        
        # Create reviews
        self.seed_reviews(properties, users)
        
        # Create payments
        self.seed_payments(bookings)
        
        # Create messages
        self.seed_messages(users)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully seeded database with sample data!')
        )

    def clear_data(self):
        """Clear all existing data"""
        Message.objects.all().delete()
        Payment.objects.all().delete()
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Property.objects.all().delete()
        Listing.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write('Existing data cleared.')

    def seed_users(self):
        """Create sample users"""
        self.stdout.write('Creating users...')
        
        # Create admin user
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@travelapp.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            phone_number='+1234567890',
            role=User.Role.ADMIN,
            is_staff=True,
            is_superuser=True
        )
        
        # Create host users
        hosts = []
        host_names = [
            ('John', 'Smith', 'john.smith@email.com', '+1111111111'),
            ('Sarah', 'Johnson', 'sarah.johnson@email.com', '+2222222222'),
            ('Mike', 'Wilson', 'mike.wilson@email.com', '+3333333333'),
            ('Emma', 'Brown', 'emma.brown@email.com', '+4444444444'),
            ('David', 'Davis', 'david.davis@email.com', '+5555555555'),
        ]
        
        for first_name, last_name, email, phone in host_names:
            host = User.objects.create_user(
                username=f"{first_name.lower()}.{last_name.lower()}",
                email=email,
                password='password123',
                first_name=first_name,
                last_name=last_name,
                phone_number=phone,
                role=User.Role.HOST
            )
            hosts.append(host)
        
        # Create guest users
        guests = []
        guest_names = [
            ('Alice', 'Williams', 'alice.williams@email.com', '+6666666666'),
            ('Bob', 'Miller', 'bob.miller@email.com', '+7777777777'),
            ('Carol', 'Taylor', 'carol.taylor@email.com', '+8888888888'),
            ('Daniel', 'Anderson', 'daniel.anderson@email.com', '+9999999999'),
            ('Eva', 'Thomas', 'eva.thomas@email.com', '+1010101010'),
            ('Frank', 'Jackson', 'frank.jackson@email.com', '+1212121212'),
            ('Grace', 'White', 'grace.white@email.com', '+1313131313'),
            ('Henry', 'Harris', 'henry.harris@email.com', '+1414141414'),
        ]
        
        for first_name, last_name, email, phone in guest_names:
            guest = User.objects.create_user(
                username=f"{first_name.lower()}.{last_name.lower()}",
                email=email,
                password='password123',
                first_name=first_name,
                last_name=last_name,
                phone_number=phone,
                role=User.Role.GUEST
            )
            guests.append(guest)
        
        self.stdout.write(f'Created {len(hosts) + len(guests) + 1} users')
        return {'admin': admin_user, 'hosts': hosts, 'guests': guests}

    def seed_properties(self, users):
        """Create sample properties"""
        self.stdout.write('Creating properties...')
        
        properties = []
        property_data = [
            ('Cozy Beach House', 'A beautiful beachfront property with stunning ocean views', 'Miami, FL', 150.00),
            ('Mountain Cabin Retreat', 'Peaceful cabin nestled in the mountains with hiking trails nearby', 'Aspen, CO', 200.00),
            ('Urban Loft', 'Modern loft in the heart of downtown with city skyline views', 'New York, NY', 180.00),
            ('Historic Townhouse', 'Charming historic townhouse with original architectural details', 'Boston, MA', 220.00),
            ('Lakefront Villa', 'Luxurious villa on the lake with private dock and boat access', 'Lake Tahoe, CA', 350.00),
            ('Desert Oasis', 'Unique desert property with swimming pool and cactus garden', 'Phoenix, AZ', 120.00),
            ('Countryside Farmhouse', 'Rustic farmhouse surrounded by rolling hills and farmland', 'Napa Valley, CA', 160.00),
            ('Tropical Paradise', 'Beachside bungalow with palm trees and tropical gardens', 'Hawaii, HI', 280.00),
            ('Ski Lodge', 'Cozy lodge near ski slopes with fireplace and hot tub', 'Park City, UT', 250.00),
            ('Wine Country Estate', 'Elegant estate in wine country with vineyard views', 'Sonoma, CA', 400.00),
        ]
        
        for i, (name, description, location, price) in enumerate(property_data):
            host = users['hosts'][i % len(users['hosts'])]
            property_obj = Property.objects.create(
                host_id=host,
                name=name,
                description=description,
                location=location,
                price_per_night=Decimal(str(price))
            )
            properties.append(property_obj)
        
        self.stdout.write(f'Created {len(properties)} properties')
        return properties

    def seed_listings(self):
        """Create sample listings"""
        self.stdout.write('Creating listings...')
        
        listings = []
        listing_data = [
            ('Vacation Rental Package', 'Complete vacation rental with all amenities included', 299.99),
            ('Weekend Getaway Deal', 'Perfect weekend escape with special pricing', 199.99),
            ('Luxury Stay Experience', 'Premium accommodation with concierge services', 599.99),
            ('Budget-Friendly Option', 'Affordable accommodation for budget-conscious travelers', 89.99),
            ('Family Package Deal', 'Family-friendly accommodation with extra space', 349.99),
        ]
        
        for title, description, price in listing_data:
            listing = Listing.objects.create(
                title=title,
                description=description,
                price=Decimal(str(price))
            )
            listings.append(listing)
        
        self.stdout.write(f'Created {len(listings)} listings')
        return listings

    def seed_bookings(self, properties, users):
        """Create sample bookings"""
        self.stdout.write('Creating bookings...')
        
        bookings = []
        statuses = [Booking.Status.PENDING, Booking.Status.CONFIRMED, Booking.Status.CANCELLED]
        
        # Create bookings for each property
        for property_obj in properties:
            # Create 2-4 bookings per property
            num_bookings = random.randint(2, 4)
            
            for _ in range(num_bookings):
                guest = random.choice(users['guests'])
                status = random.choice(statuses)
                
                # Generate random dates
                start_date = date.today() + timedelta(days=random.randint(1, 30))
                duration = random.randint(1, 14)  # 1-14 nights
                end_date = start_date + timedelta(days=duration)
                
                total_price = property_obj.price_per_night * duration
                
                booking = Booking.objects.create(
                    property_id=property_obj,
                    user_id=guest,
                    start_date=start_date,
                    end_date=end_date,
                    total_price=total_price,
                    status=status
                )
                bookings.append(booking)
        
        self.stdout.write(f'Created {len(bookings)} bookings')
        return bookings

    def seed_reviews(self, properties, users):
        """Create sample reviews"""
        self.stdout.write('Creating reviews...')
        
        reviews = []
        review_comments = [
            'Excellent property with amazing views!',
            'Perfect location and very clean accommodations.',
            'Great host, very responsive and helpful.',
            'Beautiful property, would definitely stay again.',
            'Good value for money, comfortable stay.',
            'Outstanding experience, highly recommended!',
            'Nice property but could use some improvements.',
            'Fantastic location, walking distance to everything.',
            'Clean and well-maintained, great amenities.',
            'Wonderful host, made our stay memorable.',
        ]
        
        # Create reviews for properties that have bookings
        for property_obj in properties:
            # Create 1-3 reviews per property
            num_reviews = random.randint(1, 3)
            reviewed_users = set()
            
            for _ in range(num_reviews):
                # Get a guest who has booked this property
                bookings = Booking.objects.filter(property_id=property_obj)
                if not bookings.exists():
                    continue
                    
                booking = random.choice(bookings)
                guest = booking.user_id
                
                # Avoid duplicate reviews from same user
                if guest in reviewed_users:
                    continue
                reviewed_users.add(guest)
                
                rating = random.randint(3, 5)  # Mostly positive reviews
                comment = random.choice(review_comments)
                
                review = Review.objects.create(
                    property_id=property_obj,
                    user_id=guest,
                    rating=rating,
                    comment=comment
                )
                reviews.append(review)
        
        self.stdout.write(f'Created {len(reviews)} reviews')
        return reviews

    def seed_payments(self, bookings):
        """Create sample payments"""
        self.stdout.write('Creating payments...')
        
        payments = []
        payment_methods = [Payment.PaymentMethod.CREDIT_CARD, Payment.PaymentMethod.PAYPAL, Payment.PaymentMethod.STRIPE]
        
        # Create payments for confirmed bookings
        confirmed_bookings = [b for b in bookings if b.status == Booking.Status.CONFIRMED]
        
        for booking in confirmed_bookings:
            # Some bookings might have multiple payments (partial payments)
            num_payments = random.randint(1, 2)
            
            for _ in range(num_payments):
                payment_method = random.choice(payment_methods)
                # For partial payments, amount might be less than total
                if num_payments > 1:
                    amount = booking.total_price * Decimal('0.5')  # 50% payment
                else:
                    amount = booking.total_price
                
                payment = Payment.objects.create(
                    booking_id=booking,
                    amount=amount,
                    payment_method=payment_method
                )
                payments.append(payment)
        
        self.stdout.write(f'Created {len(payments)} payments')
        return payments

    def seed_messages(self, users):
        """Create sample messages"""
        self.stdout.write('Creating messages...')
        
        messages = []
        message_templates = [
            'Hi! I am interested in booking your property. Is it available for the dates I selected?',
            'Thank you for the quick response! I would like to proceed with the booking.',
            'Could you provide more information about the amenities and nearby attractions?',
            'Perfect! I have made the payment. Looking forward to our stay.',
            'Thank you for hosting us! We had a wonderful time and would love to come back.',
            'Is there a late check-in option available? Our flight arrives late in the evening.',
            'The property was exactly as described. Thank you for the great experience!',
            'Could you recommend some good restaurants in the area?',
            'We will be arriving around 3 PM. Is early check-in possible?',
            'Thank you for being such a wonderful host. The property exceeded our expectations!',
        ]
        
        # Create messages between guests and hosts
        for host in users['hosts']:
            # Each host gets messages from 2-4 different guests
            num_guests = random.randint(2, 4)
            selected_guests = random.sample(users['guests'], min(num_guests, len(users['guests'])))
            
            for guest in selected_guests:
                # Create 2-4 message exchanges between each pair
                num_exchanges = random.randint(2, 4)
                
                for _ in range(num_exchanges):
                    # Guest sends message to host
                    guest_message = Message.objects.create(
                        sender_id=guest,
                        recipient_id=host,
                        message_body=random.choice(message_templates)
                    )
                    messages.append(guest_message)
                    
                    # Host replies (sometimes)
                    if random.choice([True, False, True]):  # 66% chance of reply
                        host_message = Message.objects.create(
                            sender_id=host,
                            recipient_id=guest,
                            message_body=f"Thank you for your message! {random.choice(['I will get back to you soon.', 'The property is available.', 'Looking forward to hosting you!'])}"
                        )
                        messages.append(host_message)
        
        self.stdout.write(f'Created {len(messages)} messages')
        return messages