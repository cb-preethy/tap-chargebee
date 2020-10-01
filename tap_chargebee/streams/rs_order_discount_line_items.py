
from tap_chargebee.streams.base import BaseChargebeeStream


class RsOrderDiscountLineItemsStream(BaseChargebeeStream):
    TABLE = 'rs_order_discount_line_items'
    ENTITY = 'order_discount_line_items'
    REPLICATION_METHOD = 'INCREMENTAL'
    REPLICATION_KEY = 'resource_updated_at'
    KEY_PROPERTIES = ['order_line_item_id', 'site_name', 'order_id', 'coupon_id']
    BOOKMARK_PROPERTIES = ['resource_updated_at']
    SELECTED_BY_DEFAULT = True
    VALID_REPLICATION_KEYS = ['resource_updated_at']
    INCLUSION = 'automatic'
    API_METHOD = 'GET'

    def get_url(self):
        return BaseChargebeeStream.CB_URL.format(self.config.get('site'))

