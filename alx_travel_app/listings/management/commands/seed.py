from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing, Booking, Review
from django.utils import timezone
from datetime import timedelta, date
import random


class Command(BaseCommand):
    help = "Seed the database with sample listings, users, bookings, and reviews"

    def handle(self, *args, **options):
        User = get_user_model()

        # Create sample users
        users = []
        for i in range(1, 4):
            username = f"seeduser{i}"
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": f"{username}@example.com"},
            )
            if created:
                user.set_password("password123")
                user.save()
            users.append(user)

        # Create sample listings
        listings_data = [
            {
                "title": "Cozy city apartment",
                "description": "A comfortable apartment in the heart of the city.",
                "address": "123 Main St",
                "price_per_night": 75.00,
                "max_guests": 2,
                "num_bedrooms": 1,
                "num_bathrooms": 1,
            },
            {
                "title": "Beach house with sea view",
                "description": "Relax on the beach and enjoy stunning sunsets.",
                "address": "456 Ocean Ave",
                "price_per_night": 250.00,
                "max_guests": 6,
                "num_bedrooms": 3,
                "num_bathrooms": 2,
            },
            {
                "title": "Mountain cabin",
                "description": "Woodsy cabin perfect for hiking and quiet weekends.",
                "address": "789 Pine Rd",
                "price_per_night": 120.00,
                "max_guests": 4,
                "num_bedrooms": 2,
                "num_bathrooms": 1,
            },
        ]

        created_listings = []
        for i, data in enumerate(listings_data):
            host = users[i % len(users)]
            listing, created = Listing.objects.get_or_create(
                title=data["title"],
                defaults={
                    "host": host,
                    "description": data["description"],
                    "address": data["address"],
                    "price_per_night": data["price_per_night"],
                    "max_guests": data["max_guests"],
                    "num_bedrooms": data["num_bedrooms"],
                    "num_bathrooms": data["num_bathrooms"],
                },
            )
            created_listings.append(listing)

        # Create sample bookings and reviews
        for listing in created_listings:
            # Booking 1 week from now for 3 nights
            start = date.today() + timedelta(days=7)
            end = start + timedelta(days=3)
            nights = (end - start).days
            total = listing.price_per_night * nights
            Booking.objects.get_or_create(
                listing=listing,
                user=users[0],
                start_date=start,
                end_date=end,
                defaults={
                    "total_price": total,
                },
            )

            # A review
            rating = random.randint(3, 5)
            Review.objects.get_or_create(
                listing=listing,
                user=users[1],
                defaults={
                    "rating": rating,
                    "comment": f"Nice stay: {listing.title}",
                },
            )

        self.stdout.write(self.style.SUCCESS("Seeding complete."))
