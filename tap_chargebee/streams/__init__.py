from .rs_applied_credits import RsAppliedCreditsStream
from .rs_coupons import RsCouponsStream
from .rs_credit_note_discount_lines import RsCreditNoteDiscountLinesStream
from .rs_credit_note_discounts import RsCreditNoteDiscountsStream
from .rs_credit_note_line_items import RsCreditNoteLineItemsStream
from .rs_credit_note_tax_lines import RsCreditNoteTaxLinesStream
from .rs_credit_note_taxes import RsCreditNoteTaxesStream
from .rs_credit_note_transactions import RsCreditNoteTransactionsStream
from .rs_credit_notes import RsCreditNotesStream
from .rs_customers import RsCustomersStream
from .rs_daily_subscription_histories import RsDailySubscriptionHistoriesStream
from .rs_dunning_details import RsDunningDetailsStream
from .rs_invoice_discount_lines import RsInvoiceDiscountLinesStream
from .rs_invoice_discounts import RsInvoiceDiscountsStream
from .rs_invoice_line_items import RsInvoiceLineItemsStream
from .rs_invoice_tax_lines import RsInvoiceTaxLinesStream
from .rs_invoice_taxes import RsInvoiceTaxesStream
from .rs_invoice_transactions import RsInvoiceTransactionsStream
from .rs_invoices import RsInvoicesStream
from .rs_monthly_subscription_histories import RsMonthlySubscriptionHistoriesStream
from .rs_payment_sources import RsPaymentSourcesStream
from .rs_payments import RsPaymentsStream
from .rs_products import RsProductsStream
from .rs_quarterly_subscription_histories import RsQuarterlySubscriptionHistoriesStream
from .rs_refunds import RsRefundsStream
from .rs_subscriptions import RsSubscriptionsStream
from .rs_weekly_subscription_histories import RsWeeklySubscriptionHistoriesStream
from .rs_yearly_subscription_histories import RsYearlySubscriptionHistoriesStream

AVAILABLE_STREAMS = [
    RsAppliedCreditsStream,
    RsCouponsStream,
    RsCreditNoteDiscountLinesStream,
    RsCreditNoteDiscountsStream,
    RsCreditNoteLineItemsStream,
    RsCreditNoteTaxLinesStream,
    RsCreditNoteTaxesStream,
    RsCreditNoteTransactionsStream,
    RsCreditNotesStream,
    RsCustomersStream,
    RsDailySubscriptionHistoriesStream,
    RsDunningDetailsStream,
    RsInvoiceDiscountLinesStream,
    RsInvoiceDiscountsStream,
    RsInvoiceLineItemsStream,
    RsInvoiceTaxLinesStream,
    RsInvoiceTaxesStream,
    RsInvoiceTransactionsStream,
    RsInvoicesStream,
    RsMonthlySubscriptionHistoriesStream,
    RsPaymentSourcesStream,
    RsPaymentsStream,
    RsProductsStream,
    RsQuarterlySubscriptionHistoriesStream,
    RsRefundsStream,
    RsSubscriptionsStream,
    RsWeeklySubscriptionHistoriesStream,
    RsYearlySubscriptionHistoriesStream,
]
