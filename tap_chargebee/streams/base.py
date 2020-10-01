import singer
import time
import json
import os

from .util import Util
from dateutil.parser import parse
from tap_framework.streams import BaseStream
from tap_framework.schemas import load_schema_by_name
from tap_framework.config import get_config_start_date
from tap_chargebee.state import get_last_record_value_for_table, incorporate, \
    save_state

LOGGER = singer.get_logger()

class BaseChargebeeStream(BaseStream):
    CB_URL = "https://{}.chargebee.com/api/v2/rs_data_export_resources"
    if os.environ.get('RS_API_URL'):
        CB_URL = os.environ.get('RS_API_URL')
        #CB_URL = "http://{}.localcb.in:8080/api/v2/rs_data_export_resources"
    RECORD_LIMIT = 100
    if os.environ.get('RS_API_RECORD_LIMIT'):
        RECORD_LIMIT = os.environ.get('RS_API_RECORD_LIMIT')

    STATE_FILE_NAME = os.environ.get('CB_RS_STATE_FILE_NAME')
    def write_schema(self):
        singer.write_schema(
            self.catalog.stream,
            self.catalog.schema.to_dict(),
            key_properties=self.KEY_PROPERTIES,
            bookmark_properties=self.BOOKMARK_PROPERTIES)

    def generate_catalog(self):
        schema = self.get_schema()
        mdata = singer.metadata.new()

        metadata = {

            "forced-replication-method": self.REPLICATION_METHOD,
            "valid-replication-keys": self.VALID_REPLICATION_KEYS,
            "inclusion": self.INCLUSION,
            #"selected-by-default": self.SELECTED_BY_DEFAULT,
            "table-key-properties": self.KEY_PROPERTIES
        }

        for k, v in metadata.items():
            mdata = singer.metadata.write(
                mdata,
                (),
                k,
                v
            )

        for field_name, field_schema in schema.get('properties').items():
            inclusion = 'available'
            if self.TABLE.startswith("rs_"):
                inclusion = "automatic"

            if field_name in self.KEY_PROPERTIES or field_name in self.BOOKMARK_PROPERTIES:
                inclusion = 'automatic'

            mdata = singer.metadata.write(
                mdata,
                ('properties', field_name),
                'inclusion',
                inclusion
            )

        cards = singer.utils.load_json(
            os.path.normpath(
                os.path.join(
                    self.get_class_path(),
                    '../schemas/{}.json'.format("cards"))))

        refs = {"cards.json": cards}

        return [{
            'tap_stream_id': self.TABLE,
            'stream': self.TABLE,
            'schema': singer.resolve_schema_references(schema, refs),
            'metadata': singer.metadata.to_list(mdata)
        }]


#    def remove_timezone(self, record):
#        transformed_record = record
#        resource_schema = self.catalog.schema.to_dict().get('properties')
#        for item in resource_schema:
#            column_schema = resource_schema[item]
#            if column_schema.get('format') and column_schema['format'] == 'date-time':
#                if isinstance(transformed_record[item], str) and len(transformed_record[item]) > 0:
#                    transformed_record[item] = transformed_record[item].strip('Z')
#        return transformed_record

    # This overrides the transform_record method in the Fistown Analytics tap-framework package
    def transform_record(self, record):
        with singer.Transformer(integer_datetime_fmt="unix-seconds-integer-datetime-parsing") as tx:
            metadata = {}
            
                
            if self.catalog.metadata is not None:
                metadata = singer.metadata.to_map(self.catalog.metadata)

            singer_transform = tx.transform(
                record,
                self.catalog.schema.to_dict(),
                metadata)
#            return self.remove_timezone(singer_transform)
            return singer_transform

    def get_stream_data(self, data):
        entity = self.ENTITY
        return [self.transform_record(item.get(entity)) for item in data]

    def sync_data(self):
        table = self.TABLE
        api_method = self.API_METHOD
        done = False

        # Attempt to get the bookmark date from the state file (if one exists and is supplied).
        LOGGER.info('Attempting to get the most recent bookmark_date for entity {}.'.format(self.ENTITY))
        prev_state = get_last_record_value_for_table(self.state, table, 'last_offset')

        # If there is no bookmark date, fall back to using the start date from the config file.
        if prev_state is None:
            LOGGER.info('Could not locate bookmark_date from STATE file. Falling back to start_date from config.json instead.')
            bookmark_date = get_config_start_date(self.config)
            last_processed_id = 0
            last_processed_dsid = 0
        else:
            bookmark_date = prev_state['resource_updated_at']
            bookmark_date = parse(bookmark_date,ignoretz=True)
            last_processed_id = prev_state.get('last_processed_id', 0)
            last_processed_dsid = prev_state.get('last_processed_dsid', 0)

        # Convert bookmarked start date to POSIX.
        bookmark_date_posix = int(bookmark_date.timestamp())

        params = {'resource': self.ENTITY,
                  'offset': json.dumps([last_processed_id, last_processed_dsid, bookmark_date_posix]),
				  'limit': self.RECORD_LIMIT}
        bookmark_key = 'resource_updated_at'
        LOGGER.info("Querying {} starting at {}".format(table, bookmark_date))

        max_date = bookmark_date
        while not done:
            response = self.client.make_request(
                url=self.get_url(),
                method=api_method,
                params=params)

            if 'api_error_code' in response.keys():
                if response['api_error_code'] == 'configuration_incompatible':
                    LOGGER.error('{} is not configured'.format(response['error_code']))
                    break

            if not response.get('rs_data_export_resource'):
                LOGGER.error('Invalid Response. Missing rs_data_export_resource key')
                break

            records = response['rs_data_export_resource'].get('list')
            if not records:
                LOGGER.info("Final offset reached. Ending sync.")
                break
            to_write = self.get_stream_data(records)
#            if self.ENTITY == 'event':
#                for event in to_write:
#                    if event["event_type"] == 'plan_deleted':
#                        Util.plans.append(event['content']['plan'])
#                    elif event['event_type'] == 'addon_deleted':
#                        Util.addons.append(event['content']['addon'])
#                    elif event['event_type'] == 'coupon_deleted':
#                        Util.coupons.append(event['content']['coupon'])
#            if self.ENTITY == 'plan':
#                for plan in Util.plans:
#                    to_write.append(plan)
#            if self.ENTITY == 'addon':
#                for addon in Util.addons:
#                    to_write.append(addon)
#            if self.ENTITY == 'coupon':
#                for coupon in Util.coupons:
#                    to_write.append(coupon) 

            
            with singer.metrics.record_counter(endpoint=table) as ctr:
                singer.write_records(table, to_write)

                ctr.increment(amount=len(to_write))
                
                for item in to_write:
                    #if item.get(bookmark_key) is not None:
                    max_date = max(
                        max_date,
                        parse(item.get(bookmark_key),ignoretz=True)
                    )

            next_offset = response['rs_data_export_resource'].get('next_offset')
            processed_state = {'resource_updated_at': max_date, 'last_processed_id': 0, 'last_processed_dsid': 0}
            if next_offset:
                processed_state['last_processed_id'] = next_offset[0]
                processed_state['last_processed_dsid'] = next_offset[1]
            try:
                self.state = incorporate(
                    self.state, table, 'last_offset', processed_state)
                save_state(self.state, self.STATE_FILE_NAME)
            except Exception as e:
                LOGGER.error(e)
                break

            if not len(response['rs_data_export_resource'].get('next_offset')):
                LOGGER.info("Final offset reached. Ending sync.")
                done = True
            else:
                LOGGER.info("Advancing by one offset.")
                params['offset'] = json.dumps(response['rs_data_export_resource'].get('next_offset'))
                bookmark_date = max_date
#        save_state(self.state)
