from ldapdb.models.fields import (CharField, ImageField, ListField,
                                  IntegerField)
import ldapdb.models


class LdapUser(ldapdb.models.Model):
    """
    Class for representing an LDAP user entry.
    """
    # LDAP meta-data
    base_dn = "dc=sdm,dc=noao,dc=edu"
    object_classes = ['*']#, 'posixAccount','shadowAccount', 'inetOrgPerson']

    # inetOrgPerson
    email = CharField(db_column='mail', blank=True)
    phone = CharField(db_column='telephoneNumber', blank=True)
    mobile_phone = CharField(db_column='mobile', blank=True)

    # posixAccount
    uid = IntegerField(db_column='uidNumber', unique=True)
    group = IntegerField(db_column='gidNumber')
    home_directory = CharField(db_column='homeDirectory')
    username = CharField(db_column='sn', primary_key=True)
    password = CharField(db_column='userPassword')
    name = CharField(db_column='commonName')

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.full_name


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
