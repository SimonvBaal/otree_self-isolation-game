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
    players_per_group = 3
    num_rounds = 40
    endowment = c(100)
    instructions_template = 'public_goods_experiment_1/instructions.html'
    lockdown_duration = 2
    threshold_lockdown = .51
    shirking_sensitivity = 11


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
    lockdown_cost = models.CurrencyField()
    patient_zero_switch = models.BooleanField()

    def set_lockdown(self):
        # Set conditions according to treatment
        if self.session.config['condition'] == 'LF':
            # Low lockdown cost condition first
            if self.round_number <= 20:
                # Low lockdown cost condition
                self.lockdown_cost = 60
            else:
                # High lockdown cost condition
                self.lockdown_cost = 90
        else:
            # High lockdown cost condition first
            if self.round_number <= 20:
                # High lockdown cost condition
                self.lockdown_cost = 90
            else:
                # Low lockdown cost condition
                self.lockdown_cost = 60

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
                p.others_contribution_percentage = 0
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        if not self.lockdown:
            for p in self.get_players():
                p.others_contribution_percentage = (round(
            (float(self.total_contribution - p.contribution) /
             (float(len(self.get_players())-1) *
              float(4)) * 100.0), 2))

        self.contribution_percentage = (round(
            (float(self.total_contribution) /
             (float(len(self.get_players())) *
              float(4)) * 100.0), 2))

        # Infection assignment by drawing a random number every round
        random_number = random.randint(1, len(self.get_players()))
        print("the random number is:", random_number)
        self.patient_zero_switch = False
        for p in self.get_players():
            if self.round_number == 1:
                if p.id_in_group == random_number:
                    # Choose random player to be infected in round 1
                    p.infected = 1
                    print("I'm player number:", p.id_in_group, "I'm Patient Zero")
                else:
                    p.infected = 0
            elif self.round_number > 3 and \
                    self.in_round(self.round_number - 1).total_infections == 1 and \
                    self.in_round(self.round_number - 2).total_infections == 1 and not\
                    self.in_round(self.round_number - 1).patient_zero_switch and not \
                    self.in_round(self.round_number - 2).patient_zero_switch and not \
                    self.in_round(self.round_number - 3).patient_zero_switch:
                # If there are no new infections for a few rounds, we shuffle.
                self.patient_zero_switch = True
                if p.id_in_group == random_number:
                    p.infected = 1
                    print("We had to switch patient zeros, I am now patient zero:", p.id_in_group)
                else:
                    p.infected = 0
            elif self.round_number != 1 and self.in_round(self.round_number - 1).lockdown:
                if p.id_in_group == random_number:
                    p.infected = 1
                    print("We came out of lockdown, I'm now the new patient zero:", p.id_in_group)
                else:
                    p.infected = 0
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

        # Sensitivity to low self-isolation levels
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
                if p.timeout is True:
                    p.actual_payment = None
                else:
                    p.actual_payment = float(p.contribution) * .1 * float(Constants.endowment)
                if p.second_player_contribution_0 is None or p.second_player_contribution_1 is None \
                        or p.second_player_contribution_2 is None or p.second_player_contribution_3 is None \
                        or p.second_player_contribution_4 is None or p.others_prediction is None:
                    p.payoff = 0
                    print("I didn't do my hypotheticals, so no payment")
                elif p.timeout is True:
                    p.payoff = 0
                    print("I timed out so I did not get paid")
                else:
                    p.payoff = (float(Constants.endowment) - float(p.contribution) * .1 * float(Constants.endowment))

                if self.round_number == 1:
                    p.cumulative_earnings = p.payoff
                else:
                    p.cumulative_earnings += p.payoff + p.in_round(self.round_number - 1).cumulative_earnings
        else:
            # If they are in lockdown:
            for p in self.get_players():
                p.payoff = Constants.endowment - self.lockdown_cost
                if self.round_number == 1:
                    p.cumulative_earnings = p.payoff
                    self.lockdown_round = 1
                else:
                    p.cumulative_earnings += p.payoff + p.in_round(self.round_number - 1).cumulative_earnings

        self.average_earnings = sum([p.payoff for p in self.get_players()]) / len(self.get_players())
        self.total_earnings = sum([p.payoff for p in self.get_players()])
        self.end_total_infections = sum([p.infected for p in self.get_players()])


class Player(BasePlayer):
    infected = models.IntegerField()
    cumulative_earnings = models.CurrencyField(min=0, initial=0)
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
    others_contribution_percentage = models.FloatField()
    timeout = models.BooleanField(initial=False)
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
    others_prediction = models.CurrencyField(
        label="On average, how much do you think others will self-isolate in this round?",
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
