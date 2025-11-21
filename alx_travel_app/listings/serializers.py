from rest_framework import serializers
from .models import Listing, Booking


class ListingSerializer(serializers.ModelSerializer):
    host = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Listing
        fields = [
            "id",
            "host",
            "title",
            "description",
            "address",
            "price_per_night",
            "max_guests",
            "num_bedrooms",
            "num_bathrooms",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "host", "created_at", "updated_at"]


class BookingSerializer(serializers.ModelSerializer):
    listing = ListingSerializer(read_only=True)
    listing_id = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.all(), source="listing", write_only=True
    )
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "listing", "listing_id", "user", "start_date", "end_date", "total_price", "created_at"]
        read_only_fields = ["id", "listing", "user", "created_at"]
