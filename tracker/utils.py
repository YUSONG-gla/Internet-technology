def convert_currency(amount, from_currency, to_currency, exchange_rates=None):
 
    if exchange_rates is None:
        exchange_rates = {
            'USD': 1.0,
            'CNY': 6.45,
            'EUR': 0.92,
            'JPY': 110.0,
        }
    
    if from_currency == to_currency:
        return amount
    
    base_usd = amount / exchange_rates.get(from_currency, 1.0)
    converted = base_usd * exchange_rates.get(to_currency, 1.0)
    
    return round(converted, 2)
