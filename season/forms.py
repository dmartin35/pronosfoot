"""
forms for user input validation
"""
from datetime import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _

from season.models import Fixture
from season.models import Forecast
from season.models import Player
from season.models import LeagueForecast
from season.models import Team
from django.conf import settings
from tools.utils import distinct

class ForecastForm(forms.ModelForm):
    """
    A form to submit forecast corresponding to a fixture
    """
    user_id = forms.IntegerField(widget=forms.HiddenInput())
    fixture = forms.ModelChoiceField(queryset=Fixture.objects.all(),
                                     widget=forms.HiddenInput())
    score_a = forms.IntegerField(min_value=0, widget=forms.TextInput(attrs={'size':'1','maxlength':'2','class':'forecastField'}), required=False)
    score_b = forms.IntegerField(min_value=0, widget=forms.TextInput(attrs={'size':'1','maxlength':'2','class':'forecastField'}), required=False)
    
    class Meta:
        model = Forecast
        fields = ['user_id', 'fixture', 'score_a', 'score_b']
    
    def save(self):
        userid = self.cleaned_data['user_id']
        fixture = self.cleaned_data['fixture']
        score_a = self.cleaned_data['score_a']
        score_b = self.cleaned_data['score_b']
        
        #retrieve player for user id
        user = Player.objects.get(id=userid)
        
        #check fixture has not started yet
        currenttime = datetime.now()
        
        fixturetime = datetime(fixture.day.year,
                                fixture.day.month,
                                fixture.day.day,
                                fixture.hour.hour,
                                fixture.hour.minute,
                                fixture.hour.second,
                                fixture.hour.microsecond)
        
        #check if a forecast for the same fixture and user has already been saved
        forecast = Forecast.objects.filter(user=user, fixture=fixture)
        
        if currenttime < fixturetime:
            if forecast:
                #update scores for forecast instance
                forecast.update(score_a=score_a)
                forecast.update(score_b=score_b)
            else:
                #creates a new forecast instance
                forecast = Forecast(user=user,
                                    fixture=fixture,
                                    score_a=score_a,
                                    score_b=score_b)
                forecast.save()
        
        return forecast

class LeagueForecastForm(forms.ModelForm):
    """
    A form to submit league forecasts
    """
    teams_by_name = Team.objects.order_by('name').all()

    user_id = forms.IntegerField(widget=forms.HiddenInput())
    winner_midseason = forms.ModelChoiceField(queryset=teams_by_name,required=False)
    winner = forms.ModelChoiceField(queryset=teams_by_name,required=False)
    second = forms.ModelChoiceField(queryset=teams_by_name,required=False)
    third = forms.ModelChoiceField(queryset=teams_by_name,required=False)
    fourth = forms.ModelChoiceField(queryset=teams_by_name,required=False)
    fifth= forms.ModelChoiceField(queryset=teams_by_name, required=False)
    looser1 = forms.ModelChoiceField(queryset=teams_by_name,required=False)
    looser2 = forms.ModelChoiceField(queryset=teams_by_name,required=False)
    looser3 = forms.ModelChoiceField(queryset=teams_by_name,required=False)
    looser4 = forms.ModelChoiceField(queryset=teams_by_name, required=False)
    
    class Meta:
        model = LeagueForecast
        fields = ['user_id', 'winner_midseason',
                  'winner', 'second', 'third', 'fourth','fifth',
                  'looser1','looser2','looser3','looser4']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # disable edition mode, if vote limit date has expired
        readonly = datetime.now() > settings.SEASON_FORECAST_MAX_DATE
        if readonly:
            for field in ['winner_midseason', 'winner', 'second', 'third', 'fourth', 'fifth',
                          'looser1', 'looser2', 'looser3', 'looser4']:
                self.fields[field].disabled = True

    def clean(self):
        #check loosers are all different
        fields = ['looser1','looser2','looser3','looser4']
        cleaned_data = [self.cleaned_data[field] for field in fields if self.cleaned_data[field]]
        if cleaned_data != distinct(cleaned_data):
            #if some values are duplicated, 
            raise forms.ValidationError(_("Loosers must all be different."))
        
        return self.cleaned_data

    def save(self):
        userid = self.cleaned_data['user_id']
        winner_midseason = self.cleaned_data['winner_midseason']
        winner = self.cleaned_data['winner']
        second = self.cleaned_data['second']
        third = self.cleaned_data['third']
        fourth = self.cleaned_data['fourth']
        fifth = self.cleaned_data['fifth']
        looser1 = self.cleaned_data['looser1']
        looser2 = self.cleaned_data['looser2']
        looser3 = self.cleaned_data['looser3']
        looser4 = self.cleaned_data['looser4']

        #retrieve player for user id
        user = Player.objects.get(id=userid)

        #check vote limit date has not expired
        currenttime = datetime.now()
        
        #check if a forecast for the same fixture and user has already been saved
        leagueforecast = LeagueForecast.objects.filter(user=user)

        if currenttime <= settings.SEASON_FORECAST_MAX_DATE:
            if leagueforecast:
                #update forecasts
                leagueforecast.update(winner_midseason = winner_midseason)
                leagueforecast.update(winner = winner)
                leagueforecast.update(second = second)
                leagueforecast.update(third = third)
                leagueforecast.update(fourth = fourth)
                leagueforecast.update(fifth = fifth)
                leagueforecast.update(looser1 = looser1)
                leagueforecast.update(looser2 = looser2)
                leagueforecast.update(looser3 = looser3)
                leagueforecast.update(looser4 = looser4)
                
            else:
                #creates a new forecast instance
                leagueforecast = LeagueForecast(user=user,
                                                winner_midseason = winner_midseason,
                                                winner = winner,
                                                second = second,
                                                third = third,
                                                fourth = fourth,
                                                fifth=fifth,
                                                looser1 = looser1,
                                                looser2 = looser2,
                                                looser3 = looser3,
                                                looser4=looser4,
                                                )
                leagueforecast.save()
                
        return leagueforecast