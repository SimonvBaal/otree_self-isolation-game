from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class PaymentInfo(Page):
    def vars_for_template(self):
        participant = self.participant
        return {
            'completion_code': "2BC7879F"
        }


page_sequence = [PaymentInfo]
