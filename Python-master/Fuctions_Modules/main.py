from book_store import book_inventory

# Add a book to inventory
book_inventory.add_book(101, 'Python Programming', 'john mina', 2000, 5)

print(book_inventory.get_book_info(101))
