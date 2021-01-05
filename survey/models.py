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
    name_in_url = 'commencement_survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Geographical location, COVID positive test, level of concern?
    age = models.IntegerField(
        label='What is your age?', min=13, max=100
    )

    gender = models.StringField(
        choices=['Male', 'Female', 'Indeterminate/Intersex/Unspecified'],
        label='What is your sex?',
        widget=widgets.RadioSelect
    )

    covid_positive = models.BooleanField(
        choices=[
            [True, 'Yes'],
            [False, 'No']
        ],
        label='Have you ever tested positive for COVID-19'
    )

    location = models.StringField(
        choices=[
            'England',
            'Scotland',
            'Wales',
            'Northern Ireland',
            'Other'
        ],
        label='In which country do you currently reside?'
    )

    def location_error_message(self, value):
        print('country is', value)
        if value == 'Other':
            return 'If you do not reside in the UK, please go to Prolific and return your submission. Thank you!'

    reading = models.BooleanField(
        choices=[
            [True, 'Yes'],
            [False, 'No']
        ],
        label='Do you have trouble reading for any reason?'
    )

    def reading_error_message(self, value):
        print("I have trouble reading:", value)
        if value:
            return "If you have trouble reading, please go to Prolific and return your submission."

    Prolific_ID = models.StringField(
        label='''
        Please enter your Prolific ID, this is important for your payment.
        '''
    )

    attention_check = models.StringField(
        choices=['New York City',
                 'Los Angeles',
                 'Chicago',
                 'Tokyo'],
        label="Please select one of the cities"
    )
