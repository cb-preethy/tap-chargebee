from tap_chargebee.streams.base import BaseChargebeeStream


class RsInvoicesStream(BaseChargebeeStream):
    TABLE = 'rs_invoices'
    ENTITY = 'invoices'
    REPLICATION_METHOD = 'INCREMENTAL'
    REPLICATION_KEY = 'resource_updated_at'
    KEY_PROPERTIES = ['id']
    BOOKMARK_PROPERTIES = ['resource_updated_at']
    SELECTED_BY_DEFAULT = True
    VALID_REPLICATION_KEYS = ['resource_updated_at']
    INCLUSION = 'automatic'
    API_METHOD = 'GET'

    def get_url(self):
        #return 'https://{}.chargebee.com/api/v2/invoices'.format(self.config.get('site'))
        return BaseChargebeeStream.CB_URL.format(self.config.get('site'))
