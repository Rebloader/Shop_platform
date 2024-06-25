from src.api_v1.schemas.order import OrderRead


async def serialized_for_output(order: OrderRead) -> dict:
    serialized_order = {
        'dealer_name': order.dealer.name,
        'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'items': [],
        'total_price': 0,
    }
    total_price = 0
    for item in order.items:
        item_info = {
            'product_name': item.product.name,
            'quantity': item.quantity,
            'price': item.total_price
        }
        serialized_order['items'].append(item_info)
        total_price += item.total_price
    serialized_order['total_price'] = total_price
    return serialized_order
