from django.shortcuts import render
from rest_framework import viewsets
from listings.models import Listing, Booking
from listings.serializers import ListingSerializer, BookingSerializer


# Create your views here.
class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
