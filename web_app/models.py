# /Users/tamanazafar/web_app/web_app/models.py
# these Django models define tables in the associated PostgreSQL database for the web application "web_app."
# Specifically, tables named "BioDecagonMono," "BioDecagonCombo," "BioDecagonTargets,"
# "Handelsnamen_Drugs," and "UserAccessHistory" are created to store data related to Project 4 - Medical Database
from django.db import models
from django.contrib.auth.models import User


class BioDecagonMono(models.Model):
    custom_id = models.AutoField(primary_key=True)
    STITCH = models.CharField(max_length=255)
    Individual_Side_Effect = models.CharField(max_length=255)
    Side_Effect_Name = models.CharField(max_length=255)

    class Meta:
        db_table = "BioDecagonMono"
        app_label = "web_app"

    def __str__(self):
        return self.STITCH

    def side_effects_list(self):
        return [self.Side_Effect_Name]

    def get_name(self):

        try:
            name_entry = Handelsnamen_drugs.objects.get(STITCH=self.STITCH)
            return name_entry.Name
        except Handelsnamen_drugs.DoesNotExist:
            return "Unbekannter Name"


class BioDecagonCombo(models.Model):
    custom_id = models.AutoField(primary_key=True)
    STITCH1 = models.CharField(max_length=255)
    STITCH2 = models.CharField(max_length=255)
    Polypharmacy_Side_Effects = models.CharField(max_length=255)
    Side_Effect_Name = models.CharField(max_length=255)

    class Meta:
        db_table = "BioDecagonCombo"
        app_label = "web_app"

    def __str__(self):
        return f"{self.STITCH1} {self.STITCH2}"

    def side_effects_list(self):
        return [self.Side_Effect_Name]

    def get_name_stitch1(self):
        print(f"STITCH1 Wert: {self.STITCH1}")
        try:
            name_entry = Handelsnamen_drugs.objects.filter(STITCH=self.STITCH1)
            return name_entry.Name
        except Handelsnamen_drugs.DoesNotExist:
            print("STITCH1 Name nicht gefunden")
            return "Unbekannter Name für STITCH1"

    def get_name_stitch2(self):
        print(f"STITCH2 Wert: {self.STITCH2}")
        try:
            name_entry = Handelsnamen_drugs.objects.filter(STITCH=self.STITCH2)
            return name_entry.Name
        except Handelsnamen_drugs.DoesNotExist:
            print("STITCH2 Name nicht gefunden")
            return "Unbekannter Name für STITCH2"


class BioDecagonTargets(models.Model):
    STITCH = models.CharField(max_length=255)
    Gene = models.CharField(max_length=255)

    class Meta:
        db_table = "BioDecagonTargets"
        app_label = "web_app"


class Handelsnamen_drugs(models.Model):
    STITCH = models.CharField(max_length=255, primary_key=True)
    Name = models.CharField(max_length=255)

    class Meta:
        db_table = "Handelsnamen_Drugs"
        app_label = "web_app"


#######################################################################

class UserAccessHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
