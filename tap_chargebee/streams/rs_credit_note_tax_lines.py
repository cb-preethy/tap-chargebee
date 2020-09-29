from tap_chargebee.streams.base import BaseChargebeeStream


class RsCreditNoteTaxLinesStream(BaseChargebeeStream):
    TABLE = 'rs_credit_note_tax_lines'
    ENTITY = 'credit_note_tax_lines'
    REPLICATION_METHOD = 'INCREMENTAL'
    REPLICATION_KEY = 'resource_updated_at'
    KEY_PROPERTIES = ['credit_note_line_item_id', 'credit_note_id', 'site_name']
    BOOKMARK_PROPERTIES = ['resource_updated_at']
    SELECTED_BY_DEFAULT = True
    VALID_REPLICATION_KEYS = ['resource_updated_at']
    INCLUSION = 'automatic'
    API_METHOD = 'GET'

    def get_url(self):
        return BaseChargebeeStream.CB_URL.format(self.config.get('site'))

