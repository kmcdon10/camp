# coding: utf8

paypal_id = 'mcdcolleen@yahoo.com'
ipn_handler = URL('default', 'ipn', host=True, scheme=True)
paypal_return_url = URL('default', 'success', args='paypal', host=True, scheme=True)
