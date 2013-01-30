from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from plants.wiki_importer import *

class Command(BaseCommand):
    
    option_list = BaseCommand.option_list + (
    
        make_option('--category-search', '-c', dest='category_search',
            action = 'store', default=None,
            help='Scan for a category, storing pages in db'),

        make_option('--parse-pages', '-p', dest='parse_pages',
            action = 'store_true', default=False,
            help='Parses existing pages'),
    )
    
    args = '<filename>'
    help = 'Scan and parse wiki category for item with infobox or taxobox'

    def handle(self, *args, **options):

        db_name = args[0]
        
        if not options['category_search'] and not options['parse_pages']:
            raise ValueError("You must specify either -c or -p option")
        
        worker = PagesFinder(db_name)
        
        if options['category_search']:
            worker.search_category_pages(options['category_search'])
    
        if options['parse_pages']:
            worker.parse_stored_pages(drop=True)
