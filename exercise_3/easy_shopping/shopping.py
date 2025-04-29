class shopping_cart:
    def __init__(self):
        # defining the items as dict to save the quantity as well
        self.items = {}

    # this function takes new item and it's quantity
    def add_item(self, new_item, quantity):

        # lets check if the item is already there in cart or not
        if new_item in self.items:
            # if yes then we add quantity to the existing quantity
            self.items[new_item] += quantity

        # but if the item is not in the cart already
        elif new_item not in self.items:
            # then we add that new item with it's quantity
            self.items[new_item] = quantity

    # this function removes the item from the cart
    def remove_item(self, existing_item, quantity):

        # if the cart doesn't have the item 
        if existing_item not in self.items:
            # then it shows an error
            print("ERROR: Item not present in cart")

        # but if that item "existing_item" exists then we delete no. of items as given in quantity 
        elif existing_item in self.items:
            self.items[existing_item] -= quantity

    # this function is just displaying the items in the cart and also their quantity
    def display_items(self):
        # printing items
        print('ITEM\t:QUANTITY')
        for item, its_qunatity in self.items.items():
            print(f"{item}\t:{its_qunatity}")
        # there quantity
        print("Total items in the Cart: ", sum(self.items.values()))