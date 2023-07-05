from django.db import models
from django.template.defaultfilters import default
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return '%s' % self.name
    

class Player(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % self.name
    

class Fixture(models.Model):
    week = models.IntegerField()
    team_a = models.ForeignKey(Team, related_name="team_a", on_delete=models.CASCADE)
    team_b = models.ForeignKey(Team, related_name="team_b", on_delete=models.CASCADE)
    score_a = models.IntegerField(blank=True, null=True)
    score_b = models.IntegerField(blank=True, null=True)
    day = models.DateField()
    hour = models.TimeField()

    def __str__(self):
        if self.score_a is not None and self.score_b is not None:
            return '%d:%s %d-%d %s (%s %s)' % (self.week, 
                                self.team_a, self.score_a, self.score_b, 
                                self.team_b, self.day, self.hour)

        return '%d:%s - %s (%s %s)' % (self.week, self.team_a,
                                       self.team_b, self.day, self.hour)
    

class Forecast(models.Model):
    fixture = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    user = models.ForeignKey(Player, on_delete=models.CASCADE)
    score_a = models.IntegerField(blank=True, null=True)
    score_b = models.IntegerField(blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    issue = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.score_a is not None and self.score_b is not None:
            return '%s-%s:%s %d-%d %s' % (self.user, self.fixture.week,
                                          self.fixture.team_a, self.score_a, 
                                          self.score_b, self.fixture.team_b)
        return '%s-%s:%s - %s' % (self.user, self.fixture.week,
                                  self.fixture.team_a, self.fixture.team_b)


class Mailing(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    newsletter = models.BooleanField(default=True)
    reminder = models.BooleanField(default=True)
    news_key = models.CharField(max_length=50, blank=True, null=True)
    remind_key = models.CharField(max_length=50, blank=True, null=True)


class Table(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    week = models.IntegerField()
    points = models.IntegerField()
    win = models.IntegerField()
    draw = models.IntegerField()
    lose = models.IntegerField()
    goal_for = models.IntegerField()
    goal_against = models.IntegerField()


class LeagueForecast(models.Model):
    user = models.ForeignKey(Player, on_delete=models.CASCADE)
    winner_midseason = models.ForeignKey(Team, related_name="winner_midseason", blank=True, null=True, on_delete=models.SET_NULL)
    winner = models.ForeignKey(Team, related_name="winner", blank=True, null=True, on_delete=models.SET_NULL)
    second = models.ForeignKey(Team, related_name="second", blank=True, null=True, on_delete=models.SET_NULL)
    third = models.ForeignKey(Team, related_name="third", blank=True, null=True, on_delete=models.SET_NULL)
    fourth = models.ForeignKey(Team, related_name="fourth", blank=True, null=True, on_delete=models.SET_NULL)
    fifth = models.ForeignKey(Team, related_name="fifth", blank=True, null=True, on_delete=models.SET_NULL)
    sixth = models.ForeignKey(Team, related_name="sixth", blank=True, null=True, on_delete=models.SET_NULL)
    relegated1 = models.ForeignKey(Team, related_name="relegated1", blank=True, null=True, on_delete=models.SET_NULL)
    relegated2 = models.ForeignKey(Team, related_name="relegated2", blank=True, null=True, on_delete=models.SET_NULL)
    relegation_playoff1 = models.ForeignKey(Team, related_name="relegation_playoff1", blank=True, null=True, on_delete=models.SET_NULL)
    points = models.IntegerField(null=True)