# web_app/admin.py
# This "admin.py" file registers Django models for the web application in the admin interface,
# enabling management of the associated database tables.
from django.contrib import admin
from .models import BioDecagonMono, BioDecagonCombo, BioDecagonTargets, Handelsnamen_drugs, UserAccessHistory


admin.site.register(BioDecagonMono)
admin.site.register(BioDecagonCombo)
admin.site.register(BioDecagonTargets)
admin.site.register(Handelsnamen_drugs)
admin.site.register(UserAccessHistory)

