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


class Constants(BaseConstants):
    name_in_url = 'end_survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Here we can ask participants questions about their experience of the game, e.g.:
    others_feedback = models.StringField(
        label='''In full sentences: what did you think of the way the other group members played the game?'''
    )

    experiment_feedback = models.StringField(
        label='''In full sentences: what did you think of the experimental setup?'''
    )
