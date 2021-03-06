#!/usr/bin/env python
# encoding: utf-8
# @Time    : 11/6/18

__author__ = 'MiracleYoung'

import os
import functools

from app.core.exceptions import CouponException

DEBUG = True


def Const(cls):
    @functools.wraps(cls)
    def new_setattr(self, name, value):
        raise CouponException(f'Const: {name} can not be rewrite.')

    cls.__setattr__ = new_setattr

    return cls


@Const
class _BaseConfig:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOG_DIR = os.path.join(BASE_DIR, 'log')

    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(asctime)s - %(filename)s[%(lineno)d] - %(levelname)s : %(message)s'
            },
            'simple': {
                'format': '%(asctime)s - %(levelname)s : %(message)s'
            }
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'formatter': 'verbose',
                'class': 'logging.StreamHandler',
            },
            'file_handler': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'level': 'INFO',
                'formatter': 'verbose',
                'filename': os.path.join(LOG_DIR, 'coupon-site.log'),
                #        suffix: "%Y%m%d_%H%M%S.log"
                'when': 'D',
                'interval': 7,
                'backupCount': 4,
                'encoding': 'utf8'
            },
            'error_file_handler': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'ERROR',
                'formatter': 'verbose',
                'filename': os.path.join(LOG_DIR, 'error.log'),
                'maxBytes': 104857600,  # 10MB
                'backupCount': 20,
                'encoding': 'utf8',
            }

        },
        'loggers': {
            'coupon_handler': {
                'handlers': ['console', 'file_handler', 'error_file_handler'],
                'level': 'INFO',
                'propagate': True
            },
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console', 'file_handler'],
        }
    }


@Const
class _DevConfig(_BaseConfig):
    MONGO_URI = "mongodb://localhost:27017/"
    MONGO_DB = "CouponSite"
    MONGO_COLLECTION = "OriginItem"


@Const
class _ProdConfig(_BaseConfig):
    pass


@Const
class _CouponConfig:
    _dev = _DevConfig()
    _prod = _ProdConfig()
    conf = _dev if DEBUG else _prod


CouponConfig = _CouponConfig()
CouponConfig = CouponConfig.conf
