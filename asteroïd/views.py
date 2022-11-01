from datetime import datetime
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.template import loader
from django.shortcuts import get_object_or_404, render
import requests

from .forms import DatesForm
from .utils.functions import formatDate, get_all_days, passages
from .utils.constants import api_key

def results(request):
    return render(request,'asteroïd/results.html')

def dates(request):
    if request.method == 'POST':
        form = DatesForm(request.POST)
        
        if form.is_valid():
            start_date = formatDate(form.cleaned_data['start_date'])
            end_date = formatDate(form.cleaned_data['end_date'])
            all_days = get_all_days(form.cleaned_data['start_date'],form.cleaned_data['end_date'])

            if len(all_days) < 9:
                search_api_url = 'https://api.nasa.gov/neo/rest/v1/feed?start_date='+start_date+'&end_date='+end_date+'&api_key='+api_key
                response = requests.get(search_api_url)

                responses = []

                for i in range(len(all_days)):
                    responses += response.json()['near_earth_objects'][all_days[i]]
                
                infos = []
                for i in range(len(responses)):
                    # On lance une requête pour chaque astéroïde pour connaître son suivant et précédents passages
                    self_response = requests.get(responses[i]['links']['self']).json()
                    
                    ast_passages = passages(self_response,responses[i]['close_approach_data'][0]['close_approach_date'])

                    # Pour la taille estimée : moyenne entre le min et le max
                    infos.append(
                        {
                            'name':responses[i]['name'],
                            'estimated_diameter':(responses[i]['estimated_diameter']['kilometers']['estimated_diameter_max']+responses[i]['estimated_diameter']['kilometers']['estimated_diameter_min'])/2,
                            'distance':responses[i]['close_approach_data'][0]['miss_distance']['kilometers'],
                            'next_passage':ast_passages['next'],
                            'lasts_passages':ast_passages['lasts']
                        })
                
                context = {
                    'start_date':form.cleaned_data['start_date'],
                    'end_date':form.cleaned_data['end_date'],
                    'response':responses,
                    'infos':infos,
                    'days':all_days
                }
                # redirect to a new URL:
                return render(request,'asteroïd/results.html',context)

            else:
                return render(request, 'asteroïd/dates.html', {'form': form,'error':"Time window must not be longer than 7 days"})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = DatesForm()

    return render(request, 'asteroïd/dates.html', {'form': form})