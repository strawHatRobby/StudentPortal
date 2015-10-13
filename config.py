import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('USERNAME')
    MAIL_PASSWORD = os.getenv('PASSWORD')
    BPIT_MAIL_SUBJECT_PREFIX = 'BPIT Student Portal,'
    BPIT_MAIL_SENDER = 'BPIT Admin <robinfr93@gmail.com>'
    BPIT_ADMIN = os.environ.get('BPIT_ADMIN')
    POSTS_PER_PAGE = 20
    FOLLOWERS_PER_PAGE = 50
    COMMENTS_PER_PAGE = 30
    SLOW_DB_QUERY_TIME = 0.5
    DEFAULT_FILE_STORAGE = 'filesystem'
    UPLOADS_FOLDER = os.path.realpath('.') + '/static/'
    FILE_SYSTEM_STORAGE_FILE_VIEW = 'static'
    ALLOWED_EXTENSIONS = set(['json','py','jpg'])

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/test'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
