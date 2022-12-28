# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class TendaConfig(AppConfig):
    name = 'tenda'
    def ready(self):
		import tenda.signals
