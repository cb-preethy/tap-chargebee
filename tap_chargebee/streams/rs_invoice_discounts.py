from tap_chargebee.streams.base import BaseChargebeeStream


class RsInvoiceDiscountsStream(BaseChargebeeStream):
    TABLE = 'rs_invoice_discounts'
    ENTITY = 'invoice_discounts'
    REPLICATION_METHOD = 'INCREMENTAL'
    REPLICATION_KEY = 'resource_updated_at'
    KEY_PROPERTIES = ['invoice_id', 'site_name', 'coupon_id', 'discount_type']
    BOOKMARK_PROPERTIES = ['resource_updated_at']
    SELECTED_BY_DEFAULT = True
    VALID_REPLICATION_KEYS = ['resource_updated_at']
    INCLUSION = 'automatic'
    API_METHOD = 'GET'

    def get_url(self):
        return BaseChargebeeStream.CB_URL.format(self.config.get('site'))

