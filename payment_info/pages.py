from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class PaymentInfo(Page):
    def vars_for_template(self):
        participant = self.participant
        return {
            'completion_code': " " # It is possible to show participants a completion code here.
        }


page_sequence = [PaymentInfo]
