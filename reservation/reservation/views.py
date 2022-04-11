from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404
from .models import Hotel, Reservation
from .serializers import HotelSerializer, ReservationSerializer
from .pagination import CustomPagination
from rest_framework.generics import GenericAPIView
import datetime
#import requests


class HotelsListView(GenericAPIView):
    pagination_class = CustomPagination
    serializer_class = HotelSerializer
    queryset = Hotel.objects.all()

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
        return Response(status=status.HTTP_200_OK, data=data)


class ReservationsListView(APIView):
    def get(self, request):
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)

        hotel = reservations[0].hotel_id
        data = serializer.data[-1]
        days = 3
        discount = 0.1
        data.update({
            "hotel": {"hotelUid": hotel.hotelUid, "name": hotel.name,
                      "fullAddress": "Россия, Москва, Неглинная ул., 4", "stars": hotel.stars},
            "payment": {
                "status": "PAID",
                "price": (10000 * days) * (1 - discount)
            }
        })
        data['status'] = 'PAID'
        data = [data]


        return Response(status=status.HTTP_200_OK, data=data)
        #return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request):
        hotelUid = request.data["hotelUid"]
        start_date_list = list(map(int, request.data["startDate"].split('-')))
        start_date = datetime.date(start_date_list[0], start_date_list[1], start_date_list[2])
        end_date_list = list(map(int, request.data["endDate"].split('-')))
        end_date = datetime.date(end_date_list[0], end_date_list[1], end_date_list[2])
        username = request.headers['X-User-Name']
        booking_time = (end_date - start_date).days

        booking_cost = 10000 * 3

        # loyalty_response = requests.get('http://loyalty-service:8003/loyalty', headers={'X-User-Name': username})
        # if loyalty_response['status'] == 'B':
        #     discount = 0.05
        # elif loyalty_response['status'] == 'S':
        #     discount = 0.07
        # elif loyalty_response['status'] == 'G':
        #     discount = 0.1
        # else:
        #     discount = 0

        booking_cost *= 1 - 0.1

        hotel = get_object_or_404(Hotel.objects.all(), hotelUid=hotelUid)
        new_reservation = Reservation()
        new_reservation.username = username
        new_reservation.hotel_id = hotel
        new_reservation.status = 'P'
        new_reservation.startDate = start_date
        new_reservation.endDate = end_date
        new_reservation.save()

        response_json = {
          "reservationUid": new_reservation.reservationUid,
          "hotelUid": hotelUid,
          "startDate": str(start_date),
          "endDate": str(end_date),
          "discount": 10,
          "status": "PAID",
          "payment": {
            "status": "PAID",
            "price": booking_cost
          }
        }
        return Response(status=status.HTTP_200_OK, data=response_json)


class ReservationView(APIView):
    def get(self, request, uid):
        try:
            reservation = get_object_or_404(Reservation.objects.all(), reservationUid=uid)
            hotel = reservation.hotel_id
            serializer = ReservationSerializer(reservation)
            data = serializer.data
            days = 3
            discount = 0.1
            data.update({
                "hotel": {"hotelUid": hotel.hotelUid, "name": hotel.name,
                          "fullAddress": "Россия, Москва, Неглинная ул., 4", "stars": hotel.stars},
                "payment": {
                    "status": "PAID",
                    "price": (10000 * days) * (1 - discount)
                }
            })
            data['status'] = 'PAID'
            return Response(status=status.HTTP_200_OK, data=data)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND, data="Not found Reservation for ID")

