# here we are importing the both the lib from the package "easy_shopping"
from easy_shopping import calculator
from easy_shopping import shopping

##### Task 1 #####

# solving all the calculation using the package
print(calculator.add(7,5))
print(calculator.sub(34,21))
print(calculator.multiply(54,2))
print(calculator.divide(144,2))
print(calculator.divide(45,0))

gap = "\n\n"  # Hi, i am gap, I make gap
print(gap) 

shop = shopping.shopping_cart()

##### Task 2 #####

#Part 1 add three items
my_shopping_list = shop.add_item("Bread", 2)
my_shopping_list = shop.add_item("Milk", 1)
my_shopping_list = shop.add_item("Egg", 5)

#Part 2 display current items and calculate total quantity
shop.display_items()

print(gap)

#Part 3 remove item from the cart, display updated 
#cart and display updated items.

# here "remove_item" function calls the display function by itself 
shop.remove_item("Egg", 2)


