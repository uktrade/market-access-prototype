#!/usr/bin/env python

"""
Convert JSON version of EC MADB barriers (results
of download-all-ec-barriers.py script) into
Django fixture file ready for importing
"""

import argparse
import csv
import datetime
import json
import pprint

from django.utils.html import strip_tags

import sys
from barriers.models import (
    BarrierRecord, BarrierCountry, BarrierType, BarrierTypeMapping
)
from django.core.exceptions import MultipleObjectsReturned

DEBUG = False

DEFAULT_INITIAL_PK = 1

from django.core.management.base import BaseCommand, CommandError
from barriers.models import BarrierCountry, BarrierNotification, BarrierType

class Command(BaseCommand):
    help = ('Convert EC MADB JSON file into '
            'our notification fixture file format.')

    match_countries = {}
    barrier_types_by_ec_measure = {}

    def convert_ddmmyyyy_date(self, from_date):
        # for dates like "20/12/2014"
        try:
            python_from_date = datetime.datetime.strptime(from_date, "%d/%m/%Y")
        except ValueError:
            # we can have weird dates like '' and 'Emergency'
            # ignore them all, the information is covered elsewhere
            return None
        else:
            return python_from_date.strftime("%Y-%m-%d")

    def convert_ddmonyyyy_date(self, from_date):
        # for dates like "20 Dec 2014"
        try:
            python_from_date = datetime.datetime.strptime(from_date, "%d %b %Y")
        except ValueError:
            # we can have weird dates like '' and 'Emergency'
            # ignore them all, the information is covered elsewhere
            return None
        else:
            return python_from_date.strftime("%Y-%m-%d")

    def get_countries_list(self):
        self.countries_queryset = BarrierCountry.objects.all()
        self.countries_list = []
        for country in self.countries_queryset:
            self.match_countries[country.name] = country
            self.match_countries[country.official_name] = country
            official_name_without_the = country.official_name.replace("The ", "")
            self.match_countries[official_name_without_the] = country
            self.countries_list.append(country.name)
        return self.countries_list

    def strip_tags(self, text):
        stripped_text = strip_tags(text)
        # also turn &nbsp; into " "
        return stripped_text        

    def get_matching_country(self, lookup_country):
        return self.match_countries[lookup_country]

    def get_barrier_types(self):
        self.barrier_types_queryset = BarrierType.objects.all()
        self.barrier_types = []
        self.barrier_types_by_ec_measure = {}
        for barrier_type in self.barrier_types_queryset:
            self.barrier_types.append(barrier_type)
            self.barrier_types_by_ec_measure[
                barrier_type.related_ec_measure_code
            ] = barrier_type
        return self.barrier_types

    def get_barrier_type_for_ec_measure(self, measure):
        try:
            source_barrier_type = BarrierType.objects.get(barrier_source=2, barrier_code=measure['code'], is_sps=measure['sps'])
        except MultipleObjectsReturned:
            raise CommandError(
              "code {} returned two barrier types!"
              .format(lookup_ec_measure)
            )
        return source_barrier_type

    def get_barrier_type_mappings(self, barrier_type):
        mappings = BarrierTypeMapping.objects.filter(source_barrier_type=barrier_type)
        dest_barrier_types = [btype.destination_barrier_type for btype in mappings]
        if dest_barrier_types:
            return dest_barrier_types
        else:
            raise Exception("No mappings found!")

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            type=str,
            help='Source JSON file to be converted'
        )
        parser.add_argument(
            '--startpk',
            type=int,
            default=DEFAULT_INITIAL_PK,
            help='Alternative starting pk value (default is '+str(DEFAULT_INITIAL_PK)+')'
        )

    def handle(self, *args, **options):
        barrier_record_rows = []
        barrier_notification_rows = []
        data = None
        countries = self.get_countries_list()
        # barrier_types = self.get_barrier_types()
        with open(options['filename'], mode='r') as file:
            pk = options['startpk']
            madbdatarows = json.load(file)
            # madbdatarows = madbdata['publicBarriers']
            for row in madbdatarows:
                products = row['barrier_detail']['products']

                try:
                    country = self.get_matching_country(row['country'])
                except KeyError:
                    raise CommandError(
                      "country not matched: {}"
                      .format(row['country'])
                    )
                barrier_types = []
                for measure in row['measures']:
                    try:
                        source_barrier_type = self.get_barrier_type_for_ec_measure(
                            measure
                        )
                    except KeyError:
                        raise CommandError(
                          "barrier type not matched: {}"
                          .format(measure['code']+" ("+measure['name']+")")
                        )
                    try:
                        dest_barrier_types = self.get_barrier_type_mappings(
                            source_barrier_type
                        )
                    except:
                        raise CommandError(
                          "No mappings found for barrier type: {}"
                          .format(source_barrier_type)
                        )
                    for barrier_type in dest_barrier_types:
                        barrier_types.append(barrier_type.pk)
                if DEBUG:
                    print ("products:")
                    pprint.pprint (products)
                if 'products' in row and len(products) > 0 and type(products[0]) == int:
                    products_text = ''
                    product_codes = products
                elif row['products']:
                    products_text = ','.join([prod['name'] for prod in products])
                    product_codes = ','.join([str(prod['id']) for prod in products])
                if DEBUG:
                    print ("measures:")
                    pprint.pprint (row['measures'])
                external_link = 'http://madb.europa.eu/madb/'
                if row['sps']:
                    external_link += ('sps_barriers_details.htm?barrier_id={}'
                                    .format(row['barrierId']))
                else:
                    external_link += ('barriers_details.htm?barrier_id={}'
                                    .format(row['barrierId']))
                if row['barrierStatus'] == 'Active':
                    barrier_status = BarrierNotification.BARRIER_NOTIFICATION_STATUS_ACTIVE
                barrier_record_dict = {
                    'pk': pk,
                    'model': 'barriers.BarrierNotification',
                    'fields': {
                        'created_date': datetime.datetime.now().strftime("%Y-%m-%d"),
                        'updated_date': datetime.datetime.now().strftime("%Y-%m-%d"),
                        'barrier_source': 2, # hardcode the value for EC
                        'core_symbol': 'EC-MADB-'+str(row['barrierId']),
                        'barrier_symbol': 'EC-MADB-'+str(row['barrierId']),
                        'status': barrier_status,
                        'country': country.pk,
                        'barrier_types': barrier_types,
                        'title': row['title'],
                        'description': self.strip_tags(row['description']),
                        'distribution_date': self.convert_ddmonyyyy_date(row['reportedDate']),
                        'products_text': products_text,
                        'product_codes': product_codes,
                        'objectives': '',
                        'keywords': '',
                        'regions_affected': '',
                        'comments_due_date': None,
                        'document_link': '',
                        'external_link': external_link
                    }
                }
                pk += 1
                barrier_record_rows.append(barrier_record_dict)

        print(json.dumps(barrier_record_rows, indent=4))
