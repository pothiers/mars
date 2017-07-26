from django.contrib import admin
from . import models
import ldapdb.models

class LDAPGroupAdmin(admin.ModelAdmin):
    exclude = ['dn', 'objectClass']
    list_display = ['gid', 'name']

class LDAPUserAdmin(admin.ModelAdmin):
    exclude = ['dn']
    search_fields = ['lastname']
    list_display = ['username', 'lastname', 'home_directory']

    def username(self, obj):
        to_return = obj.name[1]
        return to_return

admin.site.register(models.LdapUser, LDAPUserAdmin)
