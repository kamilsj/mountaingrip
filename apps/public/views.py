from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views import View
from start.models import Trip

class PublicIndex(View):
    def get(self, request):
        return render(request, 'public/public_index.html')

class PublicProfile(View):
    def get(self, request, id):
        return render(request, 'public/public_profile.html')

class PublicTrip(View):
    def get(self, request, id):
        data = {}

        try:        
            trip = Trip.objects.get(id=id)
            if not trip.private:

                import googlemaps
                from django.conf import settings

                gkey = settings.GKEY
                gmaps = googlemaps.Client(key=gkey)
            

                if trip.cover:
                    url = trip.cover.url
                else:
                    url = 'https://mountiangrip.s3-eu-west-1.amazonaws.com/assets/default_trip_cover.jpg'

                data = {
                    'trip': trip,
                    'url': url,
                    'gmaps_key': gkey,
                }
                return render(request, 'public/public_trip.html', {'data': data})
            else:
                return redirect('/public/')
        except Exception as e:
            return redirect('/public/')
        

        