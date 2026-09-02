#create a class called Restaurant
#create subclasses: chef, server, client
#create their objects

class Restaurant:
    our_menu = {
        "MAIN COURSE": {
            "Malakwang": 7000,
            "Pilau": 9000,
            "Dek Ngo": 8000,
            "Boo": 5000,
        },

        "SNACKS": {
            "Chapati": 3000,
            "Samosas": 2000,
            "Sausages": 5000,
        }
    }

    customer_select = ""

    def __init__(self, restaurant_name):
        self.restaurant_name = restaurant_name

class Customer_Choice(Restaurant):
        def __init__(self, restaurant_name, my_choice):
            super().__init__(restaurant_name)
            self.my_choice = my_choice
            print("\nSelect what you want by typing the number or exit to quit. ")
            to_choose_from = ["Menu", "Cart", "Exit"]
            for index, item in enumerate(to_choose_from, start = 1):
                print(f"\t{index}. {item}")

            my_choice = input("\nChoice: ")

            return my_choice
            

class Manager(Restaurant):
    def __init__(self, restaurant_name, name, task):
        super().__init__(restaurant_name) 
        self.name = name
        self.task = task

    def sign_in(self):
        print(f"\n{self.name} just walked in.")
        print(f"I'll be your server for the day.")


class Chef(Restaurant):
    def __init__(self, restaurant_name, name):
        super().__init__(restaurant_name)
        self.name = name

    def kitchen_order(self):
        print(f"\n{self.name} is cooking.")

    pass

class Customer(Restaurant):
    #The cart gets filled here

    def __init__(self, restaurant_name, name):
        super().__init__(restaurant_name)
        self.name = name
        self.cart = []
    def place_order(self):
        print(f"\n{self.name} here: I'd like to place an order.")
        check_out = self.cart
        
        print(f"-" * 20)
        print(f"\tCART")
        print(f"-" * 20)
        for index, item in enumerate(check_out, start=1):
            print(f"\t{index}. {item}\n")

        #--------------------------------------------- 
        #this will display the menu for the customer
        #---------------------------------------------
    def display_menu(self):
        # print("\033[0;37;40m")
        print(f"\nWelcome to {self.restaurant_name}. ")
        print(f"Here's our Menu.")
        print(f" ")
        print(f"=" * 21)
        print(f"\tMENU")
        print(f"=" * 21)

        for foods in self.our_menu:
            print(f"\n{foods} ")
            for new_item, price in self.our_menu[foods].items():
                print(f"\t{new_item}: {price}")
            # for food, price in self.our_menu[category].items():
            #     print(f"{food}: {price}")



class Server(Restaurant):
    def __init__(self, restaurant_name, name):
        super().__init__(restaurant_name)
        self.name = name
    def take_order(self):
        print(f"My name is {self.name}.")
        print(f"I'll be your server for the day.")
    pass


new_choice = Customer_Choice("Jukon")

my_customer = Customer("Jukon", "Odong")
my_customer.display_menu()
client1 = Customer("Jukon", "Byron")
client1.place_order()



