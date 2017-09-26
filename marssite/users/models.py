from ldapdb.models.fields import (CharField, ImageField, ListField,
                                  IntegerField)
import ldapdb.models

"""
there are issues I cannot work around using this library.
LDAP houses the key in a list field. There is no way to define the primary key from
a list field for django model support.

Either I'd have to write my own admin, or change LDAP schema....

"""

class LdapUser(ldapdb.models.Model):
    """
    Class for representing an LDAP user entry.
    """
    # LDAP meta-data
    base_dn = "dc=sdm,dc=noao,dc=edu"
    object_classes = ['person', 'noaoarchiveuser', 'top']



    home_directory = CharField(db_column='homeDirectory')
    lastname = CharField(db_column='sn')
    password = CharField(db_column='userPassword')
    name = ListField(db_column='cn', primary_key=True)
    lastname = ListField(db_column='sn')
    def __str__(self):
        return self.name[0]

    def __unicode__(self):
        return self.lastname


class LdapGroup(ldapdb.models.Model):
    """
    Class for representing an LDAP group entry.
    """
    # LDAP meta-data
    base_dn = "ou=groups,dc=example,dc=org"
    object_classes = ['posixGroup']

    # posixGroup attributes
    gid = IntegerField(db_column='gidNumber', unique=True)
    name = CharField(db_column='cn', max_length=200, primary_key=True)
    usernames = ListField(db_column='memberUid')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
