from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class ConsentPage(Page):
    pass


class ExplanatorySheet(Page):
    pass


page_sequence = [ConsentPage]
