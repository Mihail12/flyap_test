# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class Negotiator(AbstractUser):
    class Meta:
        verbose_name = _('negotiator')
        verbose_name_plural = _('negotiators')
