from django.shortcuts import render, redirect
from django.views import View
from func.site_functions.desire import DesireClass
from apps.desire.models import Desire, DesireSearch

from django.utils.translation import gettext as _
from django.db.models import F

from datetime import date, datetime, timedelta

class DesireView(View):

    def get(self, request):
        data = {}
             
        if request.method == 'GET' and request.user.is_authenticated:
            if 'desire' in request.GET and 'how' in request.GET and 'what' in request.GET:            
                desire = request.GET['desire']
                how = request.GET['how']
                what = request.GET['what']
                lang = request.LANGUAGE_CODE
                # some intro changes
                d = DesireClass(int(how), int(what), str(desire), request.user)
                query = desire.lower()

                # save desire
                already_is = Desire.objects.filter(desire__icontains=query)          
                if not already_is.exists():
                    Desire(user=request.user, desire=desire, how=how, what=what, lang=lang).save()
                else:
                    desire_data = already_is.get()                                
                    if not DesireSearch.objects.filter(user=request.user, desire=desire_data).exists():
                        DesireSearch(user=request.user, desire=desire_data).save()
                    else:
                        # add parameter when it was already added few mintues
                                                
                        DesireSearch.objects.filter(user=request.user, desire=desire_data).update(count=F('count')+1)
                
                left_panel_trip = d.TripData()
                left_panel_user = d.UserData()
                results = d.SearchResults()
                how_data = d.ParseHow()
                what_data = d.ParseWhat()

                print(results)
                data = {
                    'user': request.user,
                    'query': desire,
                    'how': how_data,
                    'what': what_data,
                    'left_panel_trip': left_panel_trip,
                    'left_panel_user': left_panel_user,
                    'results': results,
                }
            else:
                return redirect('/')    
        else:
            return redirect('/')

        return render(request, 'desire/index.html', {'data': data})

    def post(self, request):
        pass