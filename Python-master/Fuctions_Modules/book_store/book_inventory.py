# inventory for books
inventory = {}

def add_book(book_id, title, author, price, quantity):
    inventory[book_id] = {
        'title': title,
        'author': author,
        'price': price,
        'quantity': quantity
    }

def remove_book(book_id):
    return inventory.pop(book_id, None)

def update_quantity(book_id, quantity):
    if book_id in inventory:
        inventory[book_id]['quantity'] = quantity
        return True
    return False

def get_book_info(book_id):
    return inventory.get(book_id, None)
