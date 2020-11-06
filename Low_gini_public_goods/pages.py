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


class StartWaitPage(WaitPage):
    group_by_arrival_time = True

    def is_displayed(self):
        return self.round_number == 1


class NewRound(WaitPage):
    after_all_players_arrive = 'set_lockdown'
    body_text = 'Waiting for the other players to click through.'


class EndowmentMessage(Page):
    def is_displayed(self):
        if self.round_number == 1 or self.round_number == 11 or self.round_number == 21 or self.round_number == 31:
            return True
        else:
            return False

    def get_timeout_seconds(self):
        return 30


class LockDownMessage(Page):
    def is_displayed(self):
        # display the page when in lockdown
        if self.group.lockdown:
            return True
        else:
            return False

    def get_timeout_seconds(self):
        if self.group.lockdown_number == 1 and self.group.lockdown_round == 1:
            return 20
        else:
            return 10


class SecondPlayerContribute(Page):
    timer_text = "Time left to submit your decisions:"

    def is_displayed(self):
        if self.group.lockdown:
            return False
        else:
            return True

    def get_timeout_seconds(self):
        if self.round_number == 1:
            return 90
        else:
            return 30

    def before_next_page(self):
        if self.timeout_happened:
            self.player.second_player_contribution_0 = 5
            self.player.second_player_contribution_1 = 5
            self.player.second_player_contribution_2 = 5
            self.player.second_player_contribution_3 = 5
            self.player.second_player_contribution_4 = 5

    form_model = 'player'
    form_fields = ['second_player_contribution_0',
                   'second_player_contribution_1',
                   'second_player_contribution_2',
                   'second_player_contribution_3',
                   'second_player_contribution_4']


class Contribute(Page):
    timer_text = "Time left to submit your decision:"

    def is_displayed(self):
        if self.group.lockdown:
            return False
        else:
            return True

    def get_timeout_seconds(self):
        if self.round_number == 1:
            return 45
        else:
            return 15

    def before_next_page(self):
        if self.timeout_happened:
            self.player.contribution = 4

    form_model = 'player'
    form_fields = ['contribution']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'
    body_text = "Waiting for other participants."


class Results(Page):

    def get_timeout_seconds(self):
        if self.round_number == 1:
            return 30
        else:
            return 10


class FinalResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def get_timeout_seconds(self):
        return 30


page_sequence = [StartWaitPage, Introduction,
                 NewRound, EndowmentMessage,
                 LockDownMessage, SecondPlayerContribute,
                 Contribute, ResultsWaitPage,
                 Results, FinalResults]
