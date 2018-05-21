#!/usr/bin/python

# coding: utf-8

import os
import argparse
import getpass

from deploy import (
    prompt, confirm, config_path,
    create_virtualenv, install_requirements,
    create_env_file, create_user_config_file,
    delete_common_files, logger,
    setup_npm_tools,
)
from deploy.settings import ENV_FILE, PROJECT_NAME, SOURCES_DIR


def ask_username(question=None):
    return prompt(
        question or 'Имя пользователя', default=getpass.getuser())


def bootstrap_production():
    delete_common_files()
    create_virtualenv()

    install_requirements('production.txt')

    create_env_file(
        settings_module=config_path('production'),
    )


def bootstrap_development():
    delete_common_files()
    setup_npm_tools()
    create_virtualenv()

    install_requirements('local.txt')
    settings_format = 'local_{}'

    if confirm('Создать новую конфигурацию проекта для разработки?'):
        settings = settings_format.format(ask_username())
        create_user_config_file(settings)
    else:
        settings = settings_format.format(getpass.getuser())

    create_env_file(
        settings_module=config_path(settings),
    )

    logger.info('Для запуска проекта осталось:')
    logger.info('\t - указать конфигурацию БД в {}'.format(ENV_FILE))
    managepy_path = os.path.join(SOURCES_DIR, 'manage.py')
    logger.info('\t - выполнить {} migrate'.format(managepy_path))
    logger.info('\t - выполнить {} runserver, либо gulp'.format(managepy_path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deploy project')
    parser.add_argument('-p', '--production', dest='production',
                        action='store_const', const=True,
                        default=False)

    args = parser.parse_args()

    if args.production:
        logger.info('Проект разворачивается для продакшена.')
        bootstrap_production()
    else:
        logger.info('Проект разворачивается для разработки.')
        bootstrap_development()
