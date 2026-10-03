from customer import Customer


class CustomerManager:

    def __init__(self):
        self.customer_list = []

    def add_customer(self, customer):
        self.customer_list.append(customer)

    def show_customers(self):
        for customer in self.customer_list:
            print(
                customer.customer_id,
                "|",
                customer.name,
                "|",
                customer.phone,
                "|",
                customer.email
            )