#Create a Restaurant
#We shall have a waiter, manager, chef
#REstaurant Class
class Restaurant:
    def __init__(self, name, role, shift):
        self.name = name
        self.role = role
        self.shift = shift

    def manager(self, ):
        pass

    def staff(self, name, role, shift):
        pass

    def make_order(self):
        pass

staff1 = Restaurant()
staff2 = Restaurant()
staff3 = Restaurant()
staff1.staff("Corbin", "Server", "Night")

