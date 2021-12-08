from os import environ


SESSION_CONFIGS = [
    dict(
        name='Self-Isolation_Game',
        display_name="Only Self-Isolation Game",
        num_demo_participants=3, # If you want to play a demo, then make sure models.py has 3 players.
        app_sequence=['public_goods_experiment_1'],
        condition='HF',
    ),
    dict(
        name='Survey_Only',
        display_name='Survey Only',
        num_demo_participants=1,
        app_sequence=['survey', 'end_survey', 'payment_info'],
    ),
    dict(
        name='Self-Isolation_Game_LF', # Low lockdown cost first (LF)
        display_name='Self-Isolation Game (LF)',
        num_demo_participants=3,
        app_sequence=['consent', 'survey', 'self-isolation-game', 'end_survey', 'payment_info'],
        condition='LF'
    ),
    dict(
        name='Self-Isolation_Game_HF',
        display_name='Self-Isolation Game (HF)',
        num_demo_participants=3,
        app_sequence=['consent', 'survey', 'self-isolation-game', 'end_survey', 'payment_info'],
        condition='HF'
    ),

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.002, participation_fee=0.00, doc="" # Max 20 pence per round.
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = True # We use points, not currency directly

# You can make a room, this could come in handy depending on the setup.
ROOMS = [
    dict(
        name='Prolific_Room',
        display_name='Prolific: Self-Isolation Game'
    ),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Welcome.
"""

# don't share this with anybody.
SECRET_KEY = ' '

INSTALLED_APPS = ['otree']
