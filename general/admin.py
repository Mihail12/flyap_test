# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from rangefilter.filter import DateRangeFilter

from general.models import Agreement, Company, Country, Period, Status


class PeriodInLine(admin.TabularInline):
    model = Period
    fields = ('id', 'start_date', 'stop_date', 'status')
    extra = 0


@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_date', 'stop_date', 'company', 'negotiator')
    list_filter = (('start_date', DateRangeFilter), ('stop_date', DateRangeFilter),
                   'company__title', 'negotiator__username')
    search_fields = ('company__title', 'negotiator__first_name', 'negotiator__last_name')
    date_hierarchy = 'start_date'
    inlines = (PeriodInLine, )


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_date', 'stop_date', 'status', 'agreement')
    list_filter = (('start_date', DateRangeFilter), ('stop_date', DateRangeFilter), 'status')
    date_hierarchy = 'start_date'


class AgreementInLine(admin.TabularInline):
    model = Agreement
    fields = ('id', 'start_date', 'stop_date', 'debit', 'credit')
    extra = 0


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'country')
    search_fields = ('title', 'country__name')
    inlines = (AgreementInLine,)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    search_fields = ('name', 'code')


admin.site.register(Status, admin.ModelAdmin)
