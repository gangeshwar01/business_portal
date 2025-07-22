#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import warnings
warnings.filterwarnings(
    "ignore",
    message="Pillow could not be imported - fpdf2 will not be able to add any image",
    category=UserWarning
)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'business_portal.settings')
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
