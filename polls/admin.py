from django.contrib import admin

from .models import Question

# Mise en place de l'interface admin pour Questions
admin.site.register(Question)