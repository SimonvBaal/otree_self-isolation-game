from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class PaymentInfo(Page):
    def vars_for_template(self):
        participant = self.participant
        return {
            'completion_code': "Some Prolific code"
        }


page_sequence = [PaymentInfo]
