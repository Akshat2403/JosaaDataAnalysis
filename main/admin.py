from django.contrib import admin
from .models import data
from import_export.admin import ImportExportModelAdmin
# Register your models here.


@admin.register(data)
class DataAdmin(ImportExportModelAdmin):
    pass
