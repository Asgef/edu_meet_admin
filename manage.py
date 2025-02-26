#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE', 'edu_meet_admin_panel.settings'
    )
    # Отключаем proxy_models и admin при вызове inspectdb
    if "inspectdb" in sys.argv:
        sys.modules['edu_meet_admin_panel.proxy_models'] = None
        sys.modules['edu_meet_admin_panel.admin'] = None

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
