from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from plants.import_helpers import *

class Command(BaseCommand):
    
    """
    option_list = BaseCommand.option_list + (
        make_option('--autofill-pollutants', '-p', dest='autofill_pollutants',
            action = 'store_true', default=False,
            help='Create automatically pollutants that are not found'),

        make_option('--autofill-foreign', '-f', dest='autofill_foreign',
            action = 'store_true', default=False,
            help='Create automatically foreign keys that are not found'),

        make_option('--limit-num-rows', '-l', dest='limit_num_rows',
            action = 'store', default=0,
            help='Create automatically foreign keys that are not found'),


    )
    """

    args = '<filename>'
    help = 'Import emissioni file'

    def handle(self, *args, **options):

        db_name = args[0]
        collection_name = args[1]
        import_plants_from_mongo(db_name, collection_name)
