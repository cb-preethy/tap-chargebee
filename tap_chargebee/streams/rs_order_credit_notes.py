from tap_chargebee.streams.base import BaseChargebeeStream


class RsOrderCreditNotesStream(BaseChargebeeStream):
    TABLE = 'rs_order_credit_notes'
    ENTITY = 'order_credit_notes'
    REPLICATION_METHOD = 'INCREMENTAL'
    REPLICATION_KEY = 'resource_updated_at'
    KEY_PROPERTIES = ['order_id', 'credit_note_id', 'site_name']
    BOOKMARK_PROPERTIES = ['resource_updated_at']
    SELECTED_BY_DEFAULT = True
    VALID_REPLICATION_KEYS = ['resource_updated_at']
    INCLUSION = 'automatic'
    API_METHOD = 'GET'

    def get_url(self):
        return BaseChargebeeStream.CB_URL.format(self.config.get('site'))

