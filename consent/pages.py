from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class ExplanatorySheet(Page):
    form_model = 'player'
    form_fields = ['understanding']

    def understanding_error_message(self, value):
        print('subject does not understand', value)
        if not value:
            return 'If you do not understand, please read again. ' \
                   'If you still have trouble, then please return your submission on Prolific.'


class ConsentPage(Page):
    form_model = 'player'
    form_fields = ['consent']

    def consent_error_message(self, value):
        print('values is', value)
        if not value:
            return 'If you do not consent, then please return your submission on Prolific.'


page_sequence = [ExplanatorySheet, ConsentPage]
