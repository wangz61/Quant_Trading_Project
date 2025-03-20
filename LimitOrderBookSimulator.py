import heapq # for min-heap and max-heap

class Order:
    def __init__(self, side, order_id, price, quantity, order_type):
        self.side = side
        self.order_id = order_id
        self.price = price
        self.quantity = quantity
        self.order_type = order_type
        
    def __lt__(self, other):
        # For min-heap, reverse the comparison for bids
        return self.price > other.price if self.side == 'B' else self.price < other.price
    
    def __str__(self):
        return f"Order ID: {self.order_id}, Price: {self.price}, Quantity: {self.quantity}, Type: {self.order_type}"

class OrderBook:
    def __init__(self):
        self.bids = [] # Max-heap for bids, max priority for highest price
        self.asks = [] # Min-heap for asks, min priority for lowest price
        self.orders = {} # Dictionary to store orders by order_id
        self.next_order_id = 1 # Counter for generating unique order IDs
    
    
    def add_order(self, side, price, quantity, order_type):
        order_id = self.next_order_id
        self.next_order_id += 1
        order = Order(side, order_id, price, quantity, order_type)
        
        if order_type == 'LIMIT':
            self.orders[order_id] = order
            if side == 'B':
                heapq.heappush(self.bids, order)
            else:
                heapq.heappush(self.asks, order)
            self.match_orders()
        self.display_book()      
        
    def remove_order(self, order_id):
        if order_id in self.orders:
            order = self.orders[order_id]
            if order.side == 'B':
                self.bids = [o for o in self.bids if o.order_id != order_id]
                heapq.heapify(self.bids)
            else:
                self.asks = [o for o in self.asks if o.order_id != order_id]
                heapq.heapify(self.asks)
            del self.orders[order_id]
        self.display_book()
                
    
    def match_orders(self):
        while self.bids and self.asks and self.bids[0].price >= self.asks[0].price:
            bid = self.bids[0]
            ask = self.asks[0]
            
            exec_quantity = min(bid.quantity, ask.quantity)
            exec_price = ask.price
            
            print(f"Execution: E {bid.order_id} {ask.order_id} {exec_price} {exec_quantity}")
            
            bid.quantity -= exec_quantity
            ask.quantity -= exec_quantity
            
            if bid.quantity == 0:
                heapq.heappop(self.bids)
                del self.orders[bid.order_id]
            if ask.quantity == 0:
                heapq.heappop(self.asks)
                del self.orders[ask.order_id]
                
    
    def display_book(self):
        print("\nCurrent order Book:")
        print("Bids:")
        for bid in sorted(self.bids, reverse=True):
            print(bid)
        print("---------------------")
        print("Asks:")
        for ask in sorted(self.asks):
            print(ask)
        print("\n")
        

def process_input(input_str, order_book):
    parts = input_str.split()
    cmd = parts[0]
    
    if cmd == 'A':
        _, side, price, quantity, order_type = parts
        order_book.add_order(side, float(price), int(quantity), order_type)
    elif cmd == 'X':
        _, order_id = parts
        order_book.remove(int(order_id))
        
if __name__ == "__main__":
    order_book = OrderBook()
    print("To add an order: A <side> <price> <quantity> <order_type>")
    print("    Example: A B 100.5 10 LIMIT")
    print("To remove an order: X <order_id>")
    print("    Example: X 1")
    print("Type your commands below:")
    
    while True:
        input_str = input()
        process_input(input_str, order_book)