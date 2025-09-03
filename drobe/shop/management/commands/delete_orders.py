from shop.models import Order

class DeleteNullOrders():
    help = "This deletes all orders without transaction ids."
    
    @staticmethod
    def null_orders():
        null_orders = Order.objects.filter(transaction_id=None)
        print("\n\n", null_orders)
        null_orders.delete()
        print("null orders deleted\n\n")
        
