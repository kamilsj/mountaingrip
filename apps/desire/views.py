from django.shortcuts import render, redirect
from django.views import View
from func.site_functions.desire import DesireClass
from apps.desire.models import Desire, DesireSearch

class DesireView(View):

    def get(self, request):
        data = {}
             
        if request.method == 'GET':
            desire = request.GET['desire']
            how = request.GET['how']
            what = request.GET['what']
            lang = request.LANGUAGE_CODE
            # some intro changes
            d = DesireClass(how, what, desire)
            query = desire.lower()

            # save desire
            already_is = Desire.objects.filter(desire__icontains=query)
            if not already_is.exists():
                Desire(user=request.user, desire=desire, how=how, what=what, lang=lang).save()
            else:
                desire_data = already_is.all()
                DesireSearch(user=request.user, desire=desire_data.pk).save() 

            data = {
                'query': desire,
            }

        return render(request, 'desire/index.html', {'data': data})

    def post(self, request):
        pass