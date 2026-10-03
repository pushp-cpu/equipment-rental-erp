






class RentalManager:

    def __init__(self):
        self.rental_list = []

    def add_rental(self, rental):
        self.rental_list.append(rental)

    def show_rentals(self):
        for rental in self.rental_list:
            print(
                rental.rental_id,
                "| Customer:",
                rental.customer.name,
                "| Equipment:",
                rental.equipment.name,
                "| Days:",
                rental.days,
                "| Total: ₹" + str(rental.total_amount)
            )