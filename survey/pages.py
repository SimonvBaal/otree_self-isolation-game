from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants


class Demographics(Page):
    form_model = 'player'
    form_fields = ['Prolific_ID', 'age', 'gender', 'covid_positive', 'location', 'state', 'reading']


class CognitiveReflectionTest(Page):
    form_model = 'player'
    form_fields = ['crt_widget', 'crt_lake']


page_sequence = [Demographics, CognitiveReflectionTest]
