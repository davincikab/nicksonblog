import os
import django_heroku
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

ROOT_DIR = environ.Path(__file__) - 2

env = environ.Env()

env_file = ROOT_DIR('.env')  # assume it is in project_root
env.read_env(env_file)
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'Post',
    'User',
    'markdownx',
    # 'markdownify',
    'django_filters',
    'crispy_forms',
    'coverage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, './Post/templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/eclsn/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, './Post/static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR,'./media/')
MEDIA_URL = '/media/'

# CRISPY_TEMPLATE_PACK = 'boostrap4'
CRISPY_CLASS_CONVERTERS = {'textinput': 'form-control', 'numberinput': 'form-control',
                           'select': 'form-control', 'dateinput': 'form-control',
                           'textInput': 'form-control', 'emailinput': 'form-control',
                           'textinput textInput':'form-control'
                           }


LOGIN_URL = '/user/login/'
LOGOUT_URL = '/user/logout/'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL ='/user/login/'

django_heroku.settings(locals())
