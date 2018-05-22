import os


def _setup_env():
    import site
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dating.settings.local_settings')
    site.addsitedir(os.path.dirname(__file__))
    from django import setup
    setup()


def message_server():
    _setup_env()
    from notifications_service.server import main
    main()
