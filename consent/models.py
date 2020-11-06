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


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'consent'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent = models.BooleanField(
        choices=[
            [True, 'Yes, I consent and agree to future use of my data.'],
            [False, 'No, I do not consent or agree to future use of my data.']
        ],
        label='Do you consent to your participation and future use of your data?'
    )

    understanding = models.BooleanField(
        choices=[
            [True, 'Yes, I understand the above.'],
            [False, 'No, I do not understand the above.']
        ],
        label='Do you understand the above?'
    )
