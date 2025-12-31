from django.contrib import admin
from .models import Learn_session

# Register your models here.
@admin.register(Learn_session)
class Leard_sesssionAdmin(admin.ModelAdmin):
    list_display = ['user', 'set', 'started_at', 'finished_at', 'is_finished']
    raw_id_fields = ['user']