from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age',
                   'gender',
                   'location',
                   'covid_positive',
                   'reading',
                   'Prolific_ID']


class AttentionCheck(Page):
    form_model = 'player'
    form_fields = ['attention_check']


page_sequence = [Demographics, AttentionCheck]
