from tap_chargebee.streams.base import BaseChargebeeStream


class RsAppliedCreditsStream(BaseChargebeeStream):
    TABLE = 'rs_applied_credits'
    ENTITY = 'applied_credits'
    REPLICATION_METHOD = 'INCREMENTAL'
    REPLICATION_KEY = 'resource_updated_at'
    KEY_PROPERTIES = ['site_name', 'invoice_id', 'credit_note_id', 'date']
    BOOKMARK_PROPERTIES = ['resource_updated_at']
    SELECTED_BY_DEFAULT = True
    VALID_REPLICATION_KEYS = ['resource_updated_at']
    INCLUSION = 'automatic'
    API_METHOD = 'GET'

    def get_url(self):
        return BaseChargebeeStream.CB_URL.format(self.config.get('site'))
