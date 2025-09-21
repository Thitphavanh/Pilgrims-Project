# management/commands/update_translations.py
# Create this file in one of your apps, e.g., home/management/commands/update_translations.py

from django.core.management.base import BaseCommand
from django.core.management import call_command
import os


class Command(BaseCommand):
    help = "Update translation files for all languages"

    def handle(self, *args, **options):
        # Make messages for all languages
        languages = ["en", "lo"]

        for lang in languages:
            self.stdout.write(f"Making messages for {lang}...")
            call_command("makemessages", locale=lang, verbosity=0)

        # Compile messages
        self.stdout.write("Compiling messages...")
        call_command("compilemessages", verbosity=0)

        self.stdout.write(
            self.style.SUCCESS("Successfully updated all translation files!")
        )
