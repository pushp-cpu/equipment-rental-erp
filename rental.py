class Rental:
    def __init__(self, rental_id, customer, equipment, days):
        self.rental_id = rental_id
        self.customer = customer
        self.equipment = equipment
        self.days = days

        self.total_amount = equipment.daily_rate * days