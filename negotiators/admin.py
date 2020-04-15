# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from negotiators.models import Negotiator


@admin.register(Negotiator)
class NegotiatorAdmin(UserAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined',)
    list_editable = ['is_staff', 'is_superuser', 'is_active']
