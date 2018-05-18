from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import google_auth
from datetime import datetime, time, timedelta
from .google_calendar import GoogleCalendar
from .google_maps import GoogleMaps
from .forms import SearchForm
from .utils import to_sent, parse_recurrence, to_standard

import calendar
import googlemaps


# Calendar ID variables
FOOD_CAL    = GoogleCalendar(google_auth.get_service(), 'hv4cl31tra0t7l0ggbfrev6tes@group.calendar.google.com')
DRUG_CAL    = GoogleCalendar(google_auth.get_service(), 'nu02uodssn6j0ij4o3l4rqv9dk@group.calendar.google.com')
HEALTH_CAL  = GoogleCalendar(google_auth.get_service(), 'vlqtpo7ig0mbvpmk91j8r736kk@group.calendar.google.com')
SHOWER_CAL  = GoogleCalendar(google_auth.get_service(), 'uk8elskt37v991sbe3k7qasu1k@group.calendar.google.com')
# Maps keywords to Calendar variables
var_map = {"DRUGS": DRUG_CAL, "FOOD": FOOD_CAL, "HEALTH": HEALTH_CAL, "SHOWER": SHOWER_CAL}

# Google maps variable
gmaps = GoogleMaps('AIzaSyDY3_muYN8O6uGzGGRE35Xj_OPAMVrup4g')

# Create your views here.
def index(request):

    form = SearchForm(request.GET)

    return render(
        request,
        'index.html',
        # Passes the contents of the brackets to the template
        context={'form': form},
    )

def calendars(request):
    return render(
        request,
        'calendars.html'
    )


def search(request):

    def add_distance(events):
        """
        Adds distance_value (int) and distance_text (string) to all events in an event list. Modifies list in place and
        has no return value
        :param events: list of event objects to be modified
        """
        for event in events:
            # Brackets are necessary around origins and destinations because the google API expects a list
            api_params = {'origins': [request.GET.get('locations')],
                          'destinations': [event.get('location')],
                          'units': 'imperial'}
            resp = gmaps.get_distance(**api_params)
            # If request is successful, assign the appropriate values in each event dict
            if resp['Success'] == 'OK':
                event['distance_text'] = resp['distance_text']
                event['distance_value'] = resp['distance_value']

    # Perform the get request to google api for the appropriate service and location
    now = datetime.combine(datetime.today(), time(0, 0)).isoformat() + '-08:00'
    tomorrow = (datetime.combine(datetime.today(), time(0, 0)) + timedelta(days=1)).isoformat() + '-08:00'
    api_params = {'timeMin': now, 'timeMax': tomorrow, 'singleEvents': True, 'orderBy': "startTime"}

    services = request.GET.get('services')
    if services is None:
        # If there are no search parameters, redirect to home page
        return HttpResponseRedirect('/')
    elif services not in var_map:
        # Requested service doesn't exist
        return render(request, '404.html')
    else:
        events_today = list(var_map[services].get_events(**api_params))
        add_distance(events_today)

    return render(
        request,
        'search.html',
        context={'events': events_today, 'service': request.GET.get('services')}
    )

def details(request, service=None, event_id=None):
    '''Details: returns a response with all event info'''
    '''         pretaining to an event with id 'event_id' '''

    if service in var_map:
        google_event_params = {
            'default_summary': '',
            'default_reccurence': '',
            'default_location': '1515 Ocean St, Santa Cruz, CA 95060',
            'default_description': ''
        }
        event = var_map[service].get_event(event_id, dict(), **google_event_params)
    else:
        return render(request, '404.html')

    return render(request, 'details.html', context={'title': event.summary,
                                                    'location': event.location,
                                                    'description': event.description,
                                                    'date': event.start_datetime.date,
                                                    'time': event.start_datetime.time,
                                                    'recurrence': event.reccurence
                                                    })
