from django.contrib import admin
from . import models
from django import forms
import ldapdb.models

class LdapGroupField(forms.ModelMultipleChoiceField):
    def clean(self, value):
        return value

class LdapGroupForm(forms.ModelForm):
    #members = LdapGroupField(queryset=LdapUser.objects.all(), widget=FilteredSelectMultiple('Names', is_stacked=False), required=True, to_field_name='cn')
    pass


class LDAPGroupAdmin(admin.ModelAdmin):
    exclude = ['dn', 'objectClass']
    list_display = ['gid', 'name']

class LDAPUserAdmin(admin.ModelAdmin):

    exclude = ['dn', 'password']
    search_fields = ['lastname', 'name']
    list_display = ['name','lastname', 'home_directory']

    def username(self, obj):
        to_return = obj.name[1]
        return to_return

admin.site.register(models.LdapUser, LDAPUserAdmin)
