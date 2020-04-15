# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from enum import Enum

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _


class Agreement(models.Model):
    start_date = models.DateField()
    stop_date = models.DateField()
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='agreements')
    negotiator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   null=True, related_name='agreements')
    debit = models.FileField()
    credit = models.FileField()

    def save(self, *args, **kwargs):
        if self.start_date > self.stop_date:
            raise ValueError('Agreement start date could NOT be later than stop date')
        super(Agreement, self).save(*args, **kwargs)

    def __str__(self):
        return f'CompanyID: {self.company_id}, agreement: {self.start_date}:{self.stop_date}'

    class Meta:
        verbose_name = _('agreement')
        verbose_name_plural = _('agreements')


class Period(models.Model):
    start_date = models.DateField()
    stop_date = models.DateField()
    status = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True)
    agreement = models.ForeignKey('Agreement', on_delete=models.CASCADE, related_name='periods')

    def save(self, *args, **kwargs):
        if self.start_date > self.stop_date:
            raise ValueError('Period start date could NOT be later than stop date')
        elif self.start_date < self.agreement.start_date:
            raise ValueError('Agreement start date could NOT be earlier than start date of the earliest period')
        elif self.stop_date > self.agreement.stop_date:
            raise ValueError('Agreement stop date could NOT be later than stop date of the latest period')
        intersected_periods = self.agreement.periods.filter(
            Q(start_date__lt=self.start_date, stop_date__gt=self.start_date) |
            Q(start_date__lt=self.stop_date, stop_date__gt=self.stop_date) |
            Q(start_date__lt=self.start_date, stop_date__gt=self.stop_date) |
            Q(start_date__gt=self.start_date, stop_date__lt=self.stop_date)
        )
        if intersected_periods.exists():
            raise ValueError('Inside agreement periods should not intersect')
        super(Period, self).save(*args, **kwargs)

    def __str__(self):
        return f'AgreementID: {self.agreement_id}, period: {self.start_date}:{self.stop_date}'

    class Meta:
        verbose_name = _('period')
        verbose_name_plural = _('periods')


class Company(models.Model):
    title = models.CharField(max_length=255, unique=True)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('company')
        verbose_name_plural = _('companies')


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')


class StatusChoice(Enum):
    NEW = 'New'
    ACTIVE = 'Active'
    RECONCILIATION = 'Reconciliation'
    CLOSED = 'Closed'


class Status(models.Model):
    name = models.CharField(max_length=32, default=StatusChoice.NEW, unique=True,
                            choices=[(tag.value, tag.value) for tag in StatusChoice])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('status')
        verbose_name_plural = _('statuses')
