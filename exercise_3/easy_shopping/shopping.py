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

        # but if that item "existing_item" exists in "items" and 
        # also the quantity is a integer then 
        # we delete no. of items as given in quantity using condition 
        elif existing_item in self.items and type(quantity) is int:

            # if the quantity to be deleted is more than which is in the card we through ERROR
            if self.items[existing_item] < quantity:
                print(f"ERROR: No. of {existing_item} is less to be removed")
            
            # if the quantity is not a positive number we through error again
            elif quantity < 0:
                print(f"ERROR: {quantity} is not a positive number")

            # else we are clear, we delete the no. of items and display the results     
            else:
                self.items[existing_item] -= quantity
                self.display_items()
            
        
        # if any of the item is not in a desireable datatype/format then we display error
        else:
            print("ERROR: One/Both of the values is/are not in correct format")



    # this function is just displaying the items in the cart and also their quantity
    def display_items(self):

        # printing items
        print('ITEM\t:QUANTITY')

        # we use a for loop to take all the items from the cart and print them in format
        for item, its_qunatity in self.items.items():
            if its_qunatity != 0:
                print(f"{item}\t:{its_qunatity}") # only print them if the quantity is bigger than 0
            
        # their quantity
        print("Total items in the Cart: ", sum(self.items.values()))