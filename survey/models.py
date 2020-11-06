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
    name_in_url = 'survey'
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
            'Australia', 'Other'
        ],
        label='In which country do you currently reside?'
    )

    def location_error_message(self, value):
        print('country is', value)
        if value == 'Other':
            return 'If you do not reside in Australia, please go to Prolific and return your submission. Thank you!'

    state = models.StringField(
        choices=['ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA'],
        label='In which state/territory do you currently reside?'
    )

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
        Please enter you Prolific ID, this is important for your payment.
        '''
    )

    crt_widget = models.IntegerField(
        label='''
        "If it takes 5 machines 5 minutes to make 5 widgets,
        how many minutes would it take 100 machines to make 100 widgets?"
        '''
    )

    crt_lake = models.IntegerField(
        label='''
        In a lake, there is a patch of lily pads.
        Every day, the patch doubles in size.
        If it takes 48 days for the patch to cover the entire lake,
        how many days would it take for the patch to cover half of the lake?
        '''
    )
