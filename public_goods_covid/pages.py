
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        # display the page in the first round
        if self.round_number == 1:
            return True
        else:
            return False


class NewRound(WaitPage):
    after_all_players_arrive = 'set_lockdown'
    body_text = 'Waiting for the other players to click through'


class LockdownMessage(Page):
    def is_displayed(self):
        # display the page when in lockdown
        if self.group.lockdown:
            return True
        else:
            return False


class Contribute(Page):

    def is_displayed(self):
        if self.group.lockdown:
            return False
        else:
            return True
    """Player: Choose how much to contribute"""
    form_model = 'player'
    form_fields = ['contribution']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'
    body_text = "Waiting for other participants to contribute."


class Results(Page):
    """Players payoff: How much each has earned"""


class FinalResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds



page_sequence = [Introduction, NewRound, LockdownMessage, Contribute, ResultsWaitPage, Results, FinalResults]
