# from .models import *
# Register your models here.
from django.apps import apps
from django.contrib import admin

from import_export import resources
from .models import Book

class BookResource(resources.ModelResource):

    class Meta:
        model = Book

from import_export.admin import ImportExportModelAdmin
class ReportAdmin(ImportExportModelAdmin):
     resource_class = BookResource    
# models = apps.get_models()

# for model in models:

#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass
admin.site.register(Book,ReportAdmin)
