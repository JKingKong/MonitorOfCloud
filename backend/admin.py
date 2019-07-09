from django.contrib import admin
from backend.models import *
# Register your models here.

@admin.register(SecurityGuard)
@admin.register(ExceptionsVideo)
@admin.register(ToDoExceptions)
@admin.register(Address)
class CodeAdmin(admin.ModelAdmin):
    pass

