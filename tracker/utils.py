"""
工具函数模块
处理汇率转换等辅助功能
"""


def convert_currency(amount, from_currency, to_currency, exchange_rates=None):
    """
    汇率转换函数
    
    Args:
        amount (float): 金额
        from_currency (str): 源货币代码
        to_currency (str): 目标货币代码
        exchange_rates (dict): 汇率字典
    
    Returns:
        float: 转换后的金额
    """
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
