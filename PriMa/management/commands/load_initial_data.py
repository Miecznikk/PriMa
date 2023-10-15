import logging

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load initial data into the database"
    file_names = [
        'users.json',
        'customers.json',
        'investors.json',
        'investments.json',
        'apartments.json',
        'apartments_images.json'
    ]

    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        from django.core.management import call_command
        logger.info("Flushing database")
        call_command('flush', interactive=False)
        logger.info("Database Flushed.")
        for file_name in self.file_names:
            logger.info(f"Loading file {file_name}")
            try:
                call_command('loaddata', f'fixtures/{file_name}')
            except Exception as e:
                logger.error(f"Something went wrong during loading data from fixture {file_name}: {str(e)}")
                call_command('flush', interactive=False)
                logger.error("Database cleared due to exception, script will now close")
                return
            logger.info(f"Loading file {file_name} completed")
        logger.info("Loading initial data completed with 0 errors.")
