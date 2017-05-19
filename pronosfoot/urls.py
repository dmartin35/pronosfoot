"""pronosfoot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.urls import urlpatterns as auth_urlpatterns
from season import views

# urlpatterns = [
#
#     url(r'^login/$', auth_views.login, name='login'),
#     url(r'^logout/$', auth_views.logout, name='logout'),
#     url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
#     url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
#     url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
#         auth_views.password_reset_confirm, name='password_reset_confirm'),
#     url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
# ]

urlpatterns = auth_urlpatterns + [
    url(r'^ajax/matches/(\d+)$', views.ajax_fixtures, name='ajax_fixtures_week'),
    url(r'^ajax/calendrier/(\d+)/(\d+)?$', views.ajax_calendar, name='ajax_monthly_calendar'),
    url(r'^ajax/pronos/matches/(\d+)$', views.ajax_forecasts_fixtures, name='ajax_forecasts_fixtures'),
    url(r'^ajax/pronos/matches/resultats/(\d+)$', views.ajax_forecasts_results, name='ajax_forecasts_results'),
    url(r'^ajax/pronos/saison/$', views.ajax_forecasts_league, name='ajax_forecasts_league'),
    url(r'^ajax/pronos/saison/resultats/$', views.ajax_forecasts_league_results, name='ajax_forecasts_league_results'),
    url(r'^ajax/pronos/joueurs/match/(\d+)$', views.ajax_players_forecasts_for_fixture, name='ajax_players_forecasts_fixture'),
    url(r'^ajax/tendance/(\d+)$', views.ajax_forecasts_trends_for_week, name='ajax_forecast_trends_week'),
    url(r'^ajax/classement/ligue/(\d+)$', views.ajax_league_table, name='ajax_table_league_week'),
    url(r'^ajax/classement/joueurs/(\d+)?', views.ajax_players_table, name='ajax_table_players_week'),
    url(r'^ajax/stats/equipe/(\d+)$', views.ajax_stats_team, name='ajax_stats_team'),
    url(r'^ajax/login/(.*)$', views.ajax_login, name='ajax_login'),
    url(r'^ajax/register/$', views.ajax_register, name='ajax_register'),
    url(r'^ajax/timeout/$', views.ajax_timeout, name='ajax_timeout'),
    url(r'^ajax/needlogin/$', views.ajax_need_login, name='ajax_need_login'),
    url(r'^ajax/evo/equipe/(\d+)$', views.ajax_evo_team, name='ajax_evo_team'),
    url(r'^ajax/evo/joueur/(\d+)$', views.ajax_evo_player, name='ajax_evo_player'),

    url(r'^register/$', views.register, name='register'),
    url(r'^unsubscribe/(newsletter)/(.*)$', views.unsubscribe, name='unsubscribe_newsletter'),
    url(r'^unsubscribe/(reminder)/(.*)$', views.unsubscribe, name='unsubscribe_reminder'),

    url(r'^matches/(\d+)?$', views.fixtures, name='fixtures'),
    url(r'^pronos/(\d+)?$', views.forecasts, name='forecasts'),
    url(r'^classements/$', views.tables, name='tables'),
    url(r'^stats/$', views.stats, name='stats'),

    url(r'^$', views.index, name='index'),
]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        url(r'^404/', TemplateView.as_view(template_name='404.html')),
        url(r'^500/$',  TemplateView.as_view(template_name='500.html')),
    ]
