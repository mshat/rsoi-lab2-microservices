from django.shortcuts import render
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404
import requests
from .requests_adapter import Uri


RESERVATION_SERVICE_URI = Uri(host='lab2-reservation-2.herokuapp.com')
LOYALTY_SERVICE_URI = Uri(host='lab2-loyalty.herokuapp.com', path='loyalty')


class PersonView(APIView):
    def get(self, request):
        reservation_service_uri = RESERVATION_SERVICE_URI
        reservation_service_uri.path = 'reservations'
        reservations_response = requests.get(str(reservation_service_uri))

        loyalty_service_uri = LOYALTY_SERVICE_URI
        loyalty_response = requests.get(str(loyalty_service_uri), headers={"X-User-Name": "Test Max"})
        data = {
            "reservations": reservations_response.json(),
            "loyalty": loyalty_response.json()
        }
        return Response(status=status.HTTP_200_OK, data=data)


class HotelsListView(APIView):
    def get(self, request):
        reservation_service_uri = RESERVATION_SERVICE_URI
        reservation_service_uri.path = 'hotels'
        if request.META['QUERY_STRING']:
            reservation_service_uri.query = request.META['QUERY_STRING']
        else:
            raise Exception()
        response = requests.get(str(reservation_service_uri))
        return Response(status=status.HTTP_200_OK, data=response.json())


class ReservationsListView(APIView):
    def get(self, request):
        reservation_service_uri = RESERVATION_SERVICE_URI
        reservation_service_uri.path = 'reservations'
        response = requests.get(str(reservation_service_uri))
        return Response(status=status.HTTP_200_OK, data=response.json())

    def post(self, request):
        reservation_service_uri = RESERVATION_SERVICE_URI
        reservation_service_uri.path = 'reservations'
        loyalty_service_uri = LOYALTY_SERVICE_URI

        username = request.headers["x-user-name"]
        response = requests.post(str(reservation_service_uri),
                                 data=request.body.decode('utf-8'),
                                 headers={"Content-Type": "application/json", "x-user-name": username})
        requests.patch(str(loyalty_service_uri), headers={"X-User-Name": username})
        return Response(status=status.HTTP_200_OK, data=response.json())


class ReservationView(APIView):
    def get(self, request, uid):
        reservation_service_uri = RESERVATION_SERVICE_URI
        reservation_service_uri.path = f'reservations/{uid}'

        response = requests.get(str(reservation_service_uri))
        return Response(status=status.HTTP_200_OK, data=response.json())

    def delete(self, request, uid):
        loyalty_service_uri = LOYALTY_SERVICE_URI
        username = request.headers["x-user-name"]
        requests.delete(str(loyalty_service_uri), headers={"X-User-Name": username})
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoyaltyView(APIView):
    def get(self, request):
        loyalty_service_uri = LOYALTY_SERVICE_URI
        username = request.headers["x-user-name"]
        response = requests.get(str(loyalty_service_uri), headers={"X-User-Name": username})
        return Response(status=status.HTTP_200_OK, data=response.json())

        




