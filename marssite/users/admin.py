from django.contrib import admin
from . import models
import ldapdb.models

class LDAPGroupAdmin(admin.ModelAdmin):
    exclude = ['dn', 'objectClass']
    list_display = ['gid', 'name']

class LDAPUserAdmin(admin.ModelAdmin):
    exclude = ['dn']
    search_fields = ['username', 'name']
    list_display = ['username','home_directory', 'name']

admin.site.register(models.LdapUser, LDAPUserAdmin)
