from os import environ


SESSION_CONFIGS = [
    dict(
        name='Only_Public_Goods',
        display_name="Only Public Goods",
        num_demo_participants=10,
        app_sequence=['Low_gini_public_goods'],
        condition='Eq-Lo-Hi-Po',
    ),
    dict(
        name='survey',
        display_name='survey',
        num_demo_participants=1,
        app_sequence=['survey', 'payment_info'],
    ),
    dict(
        name='Public_Goods_Game_Hi_Lo',
        display_name='Public Goods Game 2020 (Hi->Lo)',
        num_demo_participants=10,
        app_sequence=['consent', 'survey', 'Low_gini_public_goods', 'payment_info'],
        condition='Hi-Eq-Po-Lo'
    ),
    dict(
        name='Public_Goods_Game_Eq_Po',
        display_name='Public Goods Game 2020 (Eq->Po)',
        num_demo_participants=10,
        app_sequence=['consent', 'survey', 'Low_gini_public_goods', 'payment_info'],
        condition='Eq-Lo-Hi-Po'
    ),
    dict(
        name='Public_Goods_Game_Lo_Hi',
        display_name='Public Goods Game 2020 (Lo->Hi)',
        num_demo_participants=10,
        app_sequence=['consent', 'survey', 'Low_gini_public_goods', 'payment_info'],
        condition='Lo-Po-Eq-Hi'
    ),
    dict(
        name='Public_Goods_Game_Po_Eq',
        display_name='Public Goods Game 2020 (Po->Eq)',
        num_demo_participants=10,
        app_sequence=['consent', 'survey', 'Low_gini_public_goods', 'payment_info'],
        condition='Po-Hi-Lo-Eq'
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
    dict(
        name='Pilot_experiment',
        display_name='Prolific - Pilot experiment'),
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
