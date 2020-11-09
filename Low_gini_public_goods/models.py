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
A public goods game, with public health as the good and voluntary self-isolation as the contribution.
"""


class Constants(BaseConstants):
    name_in_url = 'public_goods_game'
    players_per_group = 10
    num_rounds = 40
    endowment = c(1)
    # Richest u equally share f of the income, others equally share remainder, then G = f - u. 25 = 50 - 25
    instructions_template = 'Low_gini_public_goods/instructions.html'
    lockdown_duration = 2
    threshold_lockdown = .51
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
    average_earnings = models.CurrencyField()
    lockdown = models.BooleanField(initial=False)
    lockdown_round = models.IntegerField(initial=0)
    lockdown_number = models.IntegerField(initial=0)
    number_of_players = models.IntegerField()

    def set_lockdown(self):
        # Set lockdown variables for upcoming round
        self.number_of_players = len(self.get_players())

        # Balanced square design: E = A, L = B, P = C, H = D
        if self.session.config['condition'] == 'Eq-Lo-Hi-Po':
            if self.round_number <= 10:
                # Equality Condition
                for p in self.get_players():
                    p.my_endowment = 100
            elif self.round_number >= 11 & self.round_number <= 20:
                # Low Gini Condition (Gini = 24)
                for p in self.get_players():
                    if p.id_in_group == 2 or p.id_in_group == 3 or p.id_in_group == 7 or p.id_in_group == 8:
                        p.my_endowment = 160
                    else:
                        p.my_endowment = 60
            elif self.round_number >= 21 & self.round_number <= 30:
                # High Gini Condition (Gini = 42)
                for p in self.get_players():
                    if p.id_in_group == 1 or p.id_in_group == 4 or p.id_in_group == 5:
                        p.my_endowment = 240
                    else:
                        p.my_endowment = 40
            else:
                # Poverty for all Condition
                for p in self.get_players():
                    p.my_endowment = 50
        elif self.session.config['condition'] == 'Lo-Po-Eq-Hi':
            if self.round_number <= 10:
                # Low Gini Condition (Gini = 24)
                for p in self.get_players():
                    if p.id_in_group == 2 or p.id_in_group == 3 or p.id_in_group == 7 or p.id_in_group == 8:
                        p.my_endowment = 160
                    else:
                        p.my_endowment = 60
            elif self.round_number >= 11 & self.round_number <= 20:
                # Poverty for all Condition
                for p in self.get_players():
                    p.my_endowment = 50
            elif self.round_number >= 21 & self.round_number <= 30:
                # Equality Condition
                for p in self.get_players():
                    p.my_endowment = 100
            else:
                # High Gini Condition (Gini = 42)
                for p in self.get_players():
                    if p.id_in_group == 1 or p.id_in_group == 4 or p.id_in_group == 5:
                        p.my_endowment = 240
                    else:
                        p.my_endowment = 40
        elif self.session.config['condition'] == 'Po-Hi-Lo-Eq':
            if self.round_number <= 10:
                # Poverty for all Condition
                for p in self.get_players():
                    p.my_endowment = 50
            elif self.round_number <= 20:
                # High Gini Condition (Gini = 42)
                for p in self.get_players():
                    if p.id_in_group == 1 or p.id_in_group == 4 or p.id_in_group == 5:
                        p.my_endowment = 240
                    else:
                        p.my_endowment = 40
            elif self.round_number <= 30:
                # Low Gini Condition (Gini = 24)
                for p in self.get_players():
                    if p.id_in_group == 2 or p.id_in_group == 3 or p.id_in_group == 7 or p.id_in_group == 8:
                        p.my_endowment = 160
                    else:
                        p.my_endowment = 60
            else:
                # Equality Condition
                for p in self.get_players():
                    p.my_endowment = 100
        else:
            # Hi-Eq-Po-Lo
            if self.round_number <= 10:
                # High Gini Condition (Gini = 42)
                for p in self.get_players():
                    if p.id_in_group == 1 or p.id_in_group == 4 or p.id_in_group == 5:
                        p.my_endowment = 240
                    else:
                        p.my_endowment = 40
            elif self.round_number <= 20:
                # Equality Condition
                for p in self.get_players():
                    p.my_endowment = 100
            elif self.round_number <= 20:
                # Poverty for all Condition
                for p in self.get_players():
                    p.my_endowment = 50
            else:
                # Low Gini Condition (Gini = 24)
                for p in self.get_players():
                    if p.id_in_group == 2 or p.id_in_group == 3 or p.id_in_group == 7 or p.id_in_group == 8:
                        p.my_endowment = 160
                    else:
                        p.my_endowment = 60

        if self.round_number == 1:
            self.total_infections = 1
        else:
            self.total_infections = self.in_round(self.round_number - 1).end_total_infections

        if self.total_infections < (Constants.threshold_lockdown * len(self.get_players())):
            # If less than the threshold have the virus, no lockdown.
            self.lockdown = False
            self.lockdown_round = 0
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
              float(4)) * 100.0), 2))

        # Infection assignment from last round
        for p in self.get_players():
            if self.lockdown_number < len(self.get_players()) and p.id_in_group == self.lockdown_number + 1:
                p.infected = 1
                print("I'm Patient Zero")
            elif self.lockdown_number >= len(self.get_players()) and p.id_in_group == self.lockdown_number - len(
                    self.get_players() + 1):
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
                                                   float(p.contribution) /
                                                   float(4))
                print("infection pool", infection_pool)

        # Sensitivity to shirking
        infection_pool = infection_pool / (float(len(self.get_players())) / float(Constants.shirking_sensitivity))
        print("unadjusted infection pool:", infection_pool)
        if infection_pool > 1:
            infection_pool = 1.0

        # Set new infections
        if not self.lockdown:
            for p in self.get_players():
                if p.infected == 0:
                    p.transmission_chance = round((1.0 - float(p.contribution) /
                                           float(4)) * infection_pool, 2)
                    if random.random() <= p.transmission_chance:
                        p.infected = 1
                        print("I'm now infected")
                    else:
                        p.infected = 0
                    print(p.transmission_chance, "was my chance of getting infected")
                else:
                    p.infected = 1
                    p.transmission_chance = 0

        # Set payoffs taking into account whether they're in lockdown
        if not self.lockdown:
            for p in self.get_players():
                # Set payoffs
                p.actual_payment = float(p.contribution)*.1*float(p.my_endowment)
                if p.second_player_contribution_0 == 5 or p.second_player_contribution_1 == 5\
                        or p.second_player_contribution_2 == 5 or p.second_player_contribution_3 == 5\
                        or p.second_player_contribution_4 == 5:
                    p.payoff = 0
                    print("I didn't do anything, so I don't get paid.")
                else:
                    p.payoff = (float(p.my_endowment) - float(p.contribution)*.1*float(p.my_endowment))

                if self.round_number == 1:
                    p.cumulative_earnings = p.payoff
                    print("I got money", p.payoff)
                else:
                    p.cumulative_earnings += p.payoff + p.in_round(self.round_number - 1).cumulative_earnings
                    print("I got money", p.payoff)
        else:
            # If they are in lockdown:
            for p in self.get_players():
                p.payoff = p.my_endowment * .3
                if self.round_number == 1:
                    p.cumulative_earnings = p.payoff
                    self.lockdown_round = 1
                else:
                    p.cumulative_earnings += p.payoff + p.in_round(self.round_number - 1).cumulative_earnings

        self.average_earnings = sum([p.payoff for p in self.get_players()])/len(self.get_players())
        self.total_earnings = sum([p.payoff for p in self.get_players()])
        self.end_total_infections = sum([p.infected for p in self.get_players()])

    def average_endowment(self):
        return sum([p.my_endowment for p in self.get_players()])/len(self.get_players())



class Player(BasePlayer):
    infected = models.IntegerField()
    cumulative_earnings = models.CurrencyField(min=0, initial=0)
    my_endowment = models.CurrencyField()
    actual_payment = models.CurrencyField()
    transmission_chance = models.FloatField()
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

    def payment(self):
        self.participant.earnings = self.cumulative_earnings

    def maximum_contribution(self):
        return self.my_endowment * .4