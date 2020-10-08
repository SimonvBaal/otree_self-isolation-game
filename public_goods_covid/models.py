import random

from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

author = 'Simon van Baal, Monash University'

doc = """
A public goods game, with public health as the public good and self-isolation as contribution.
"""


class Constants(BaseConstants):
    name_in_url = 'public_goods_2020' # if not working then set this back to public_goods_covid
    players_per_group = 3
    num_rounds = 10
    endowment = c(10)
    # Richest u equally share f of the income, others equally share remainder, then G = f - u. 25 = 50 - 25
    maximum_contribution = .4 * endowment
    instructions_template = 'public_goods_covid/instructions.html'
    lockdown_duration = 2
    threshold_lockdown = .51
    lockdown_earnings = .3 * endowment
    shirking_sensitivity = 4


class Subsession(BaseSubsession):

    def vars_for_admin_report(self):
        contributions = [
            p.contribution for p in self.get_players() if p.contribution is not None
        ]
        if contributions:
            return dict(
                avg_contribution=sum(contributions) / len(contributions),
                min_contribution=min(contributions),
                max_contribution=max(contributions),
            )
        else:
            return dict(
                avg_contribution='(no data)',
                min_contribution='(no data)',
                max_contribution='(no data)',
            )


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    contribution_percentage = models.FloatField()
    total_infections = models.IntegerField()
    end_total_infections = models.IntegerField()
    total_earnings = models.CurrencyField()
    lockdown = models.BooleanField(initial=False)
    lockdown_round = models.IntegerField(initial=0)
    lockdown_number = models.IntegerField(initial=0)
    number_of_players = models.IntegerField()

    def set_lockdown(self):
        # Set lockdown variables for upcoming round
        self.number_of_players = len(self.get_players())

        if self.round_number == 1:
            self.total_infections = 0
        else:
            self.total_infections = self.in_round(self.round_number - 1).end_total_infections

        if self.total_infections < (Constants.threshold_lockdown * len(self.get_players())):
            # If less than the threshold have the virus, no lockdown.
            self.lockdown = False
            self.lockdown_round = 0
            print("No lockdown, yay.")
            if self.round_number == 1:
                self.lockdown_number = 0
            else:
                self.lockdown_number = self.in_round(self.round_number - 1).lockdown_number
                print("We've had this number of lockdowns", self.lockdown_number)
        else:
            # Lockdown, unless the last round of lockdown has passed.
            if self.in_round(self.round_number - 1).lockdown_round == 0:
                self.lockdown = True
                self.lockdown_round = 1
                self.lockdown_number = self.in_round(self.round_number - 1).lockdown_number + 1
                print("First round of lockdown")
            elif self.in_round(self.round_number - 1).lockdown_round < Constants.lockdown_duration:
                self.lockdown = True
                self.lockdown_round = self.in_round(self.round_number - 1).lockdown_round + 1
                self.lockdown_number = self.in_round(self.round_number - 1).lockdown_number
                print("Lockdown Round number", self.lockdown_round)
            else:
                self.lockdown = False
                self.lockdown_round = 0
                self.lockdown_number = self.in_round(self.round_number - 1).lockdown_number
                for p in self.get_players():
                    p.infected = 0
                print("Lockdown is over, nobody is infected anymore")

    def set_payoffs(self):
        # In case of lockdown we set players' contributions to zero.
        if self.lockdown:
            for p in self.get_players():
                p.contribution = 0

        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.contribution_percentage = (round(
                 (float(self.total_contribution) /
                  (float(len(self.get_players())) *
                 float(Constants.maximum_contribution)) * 100.0), 2))

        # Infection assignment from last round
        for p in self.get_players():
            if self.lockdown_number < len(self.get_players()) and p.id_in_group == self.lockdown_number + 1:
                p.infected = 1
                print("I'm Patient Zero")
            elif self.lockdown_number >= len(self.get_players()) and p.id_in_group == self.lockdown_number - len(self.get_players() + 1):
                p.infected = 1
                print("I'm Patient Zero")
            elif self.round_number != 1 and self.in_round(self.round_number - 1).lockdown:
                p.infected = 0
                print("I'm No longer infected after lockdown")
            elif self.round_number != 1 and p.in_round(self.round_number - 1).infected == 1:
                p.infected = 1
                print("Players were infected in previous round, so they're still infected")
            else:
                p.infected = 0
                print("Else, so not infected")

        # Set infection pool, so we can determine the newly infected players
        infection_pool = float(0.0)
        for p in self.get_players():
            if p.infected == 1:
                infection_pool = infection_pool + (1.0 -
                                                   float(p.contribution)/
                                                   float(Constants.maximum_contribution))
                print("infection pool", infection_pool)

        # Sensitivity to shirking
        infection_pool = infection_pool/(float(len(self.get_players()))/float(Constants.shirking_sensitivity))
        print("unadjusted infection pool:", infection_pool)
        if infection_pool > 1:
            infection_pool = 1.0

        # Set new infections
        if not self.lockdown:
            for p in self.get_players():
                if p.infected == 0:
                    transmission_chance = (1.0 - float(p.contribution) /
                                           float(Constants.maximum_contribution)) * infection_pool
                    if random.random() <= transmission_chance:
                        p.infected = 1
                        print("I'm now infected")
                    else:
                        p.infected = 0
                    print(transmission_chance, "was my chance of getting infected")
                else:
                    p.infected = 1

        # Set payoffs taking into account whether they're in lockdown
        if not self.lockdown:
            for p in self.get_players():
                # Set payoffs
                p.payoff = (Constants.endowment - p.contribution)
                if self.round_number == 1:
                    p.cumulative_earnings = p.payoff
                    print("I got money", p.payoff)
                else:
                    p.cumulative_earnings += p.payoff + p.in_round(self.round_number - 1).cumulative_earnings
                    print("I got money", p.payoff)
        else:
            # If they are in lockdown:
            for p in self.get_players():
                p.payoff = Constants.lockdown_earnings
                if self.round_number == 1:
                    p.cumulative_earnings = p.payoff
                    self.lockdown_round = 1
                else:
                    p.cumulative_earnings += p.payoff + p.in_round(self.round_number - 1).cumulative_earnings

        self.total_earnings = sum([p.payoff for p in self.get_players()])
        self.end_total_infections = sum([p.infected for p in self.get_players()])

    def first_round(self):
        self.total_infections = 1



class Player(BasePlayer):
    contribution = models.CurrencyField(
        label="How much do you actually want to self-isolate in this round?",
        choices=[
            [0, "Not at all"],
            [1, "Slightly"],
            [2, "Moderately"],
            [3, "Stringently"],
            [4, "Completely"]
        ],
        widget=widgets.RadioSelectHorizontal
    )
    second_player_contribution_0 = models.CurrencyField(
        label="If the group self-isolation average were - Not at all",
        choices=[
            [0, "Not at all"],
            [1, "Slightly"],
            [2, "Moderately"],
            [3, "Stringently"],
            [4, "Completely"]
        ],
        widget=widgets.RadioSelectHorizontal
    )
    second_player_contribution_1 = models.CurrencyField(
        label="If the group self-isolation average were - Slightly",
        choices=[
            [0, "Not at all"],
            [1, "Slightly"],
            [2, "Moderately"],
            [3, "Stringently"],
            [4, "Completely"]
        ],
        widget=widgets.RadioSelectHorizontal
    )
    second_player_contribution_2 = models.CurrencyField(
        label="If the group self-isolation average were - Moderately",
        choices=[
            [0, "Not at all"],
            [1, "Slightly"],
            [2, "Moderately"],
            [3, "Stringently"],
            [4, "Completely"]
        ],
        widget=widgets.RadioSelectHorizontal
    )
    second_player_contribution_3 = models.CurrencyField(
        label="If the group self-isolation average were - Stringently",
        choices=[
            [0, "Not at all"],
            [1, "Slightly"],
            [2, "Moderately"],
            [3, "Stringently"],
            [4, "Completely"]
        ],
        widget=widgets.RadioSelectHorizontal
    )
    second_player_contribution_4 = models.CurrencyField(
        label="If the group self-isolation average were - Completely",
        choices=[
            [0, "Not at all"],
            [1, "Slightly"],
            [2, "Moderately"],
            [3, "Stringently"],
            [4, "Completely"]
        ],
        widget=widgets.RadioSelectHorizontal
    )
    infected = models.IntegerField()
    cumulative_earnings = models.CurrencyField(min=0, initial=0)

    def payment(self):
        self.participant.earnings = self.cumulative_earnings
