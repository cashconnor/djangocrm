from django.contrib import admin
from .models import User, Lead, Agent, UserProfile, Category


class LeadAdmin(admin.ModelAdmin):
    # fields = (
    #     'first_name',
    #     'last_name',
    # )
    list_display =['first_name', 'last_name', 'age']
    list_display_links = ['age']
    list_editable = ['first_name']

admin.site.register(Category)
admin.site.register(User)
admin.site.register(Lead, LeadAdmin)
admin.site.register(Agent)
admin.site.register(UserProfile)