from os import environ


SESSION_CONFIGS = [
    dict(
        name='Only_Public_Goods',
        display_name="Only Public Goods",
        num_demo_participants=3,
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
        name='Public_Goods_Game_LF',
        display_name='Public Goods Game 2020 (LF)',
        num_demo_participants=3,
        app_sequence=['consent', 'survey', 'public_goods_experiment_1', 'end_survey', 'payment_info'],
        condition='LF'
    ),
    dict(
        name='Public_Goods_Game_HF',
        display_name='Public Goods Game 2020 (HF)',
        num_demo_participants=3,
        app_sequence=['consent', 'survey', 'public_goods_experiment_1', 'end_survey', 'payment_info'],
        condition='HF'
    ),

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.002, participation_fee=0.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = True

ROOMS = [
    dict(
        name='Prolific_Room',
        display_name='Prolific - Public Goods Game'
    ),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""

# don't share this with anybody.
SECRET_KEY = '$@32wylmc#$v&1953*whfqh2oe!140aym*#9$iw@t00i(!%e!i'

INSTALLED_APPS = ['otree']
