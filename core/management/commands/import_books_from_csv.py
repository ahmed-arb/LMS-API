import csv
from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandParser

from core.serializers import BookSerializer
from core.models import Book


class Command(BaseCommand):
    help = "Import books form csv"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("file_path", nargs=1, type=str)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        self.file_path = options['file_path'][0]
        self.prepare()
        self.main()
        self.finalize()

    def prepare(self):
        self.imported_counter = 0
        self.skipped_counter = 0

    def main(self):
        self.stdout.write("=== Importing Books ===\n\n")

        with open(self.file_path, 'r') as f:
            reader = csv.DictReader(f)

            for index, row in enumerate(reader):
                serializer = BookSerializer(data=row)
                if serializer.is_valid():
                    self.imported_counter += 1
                    serializer.save()
                    self.stdout.write(f'{index} {row["name"]} SAVED')
                else:
                    self.skipped_counter += 1
                    self.stdout.write(f'{index} {row["name"]} SKIPPED {serializer.errors}')

    def finalize(self):
        self.stdout.write("----------------------")
        self.stdout.write(f"Books imported: {self.imported_counter}")
        self.stdout.write(f"Books skipped: {self.skipped_counter}")
