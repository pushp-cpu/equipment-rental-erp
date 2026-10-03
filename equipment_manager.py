from equipment import Equipment
from database import update_equipment_availability


class EquipmentManager:

    def __init__(self):
        self.equipment_list = []

    def add_equipment(self, equipment):
        self.equipment_list.append(equipment)

    def show_equipment(self):
        for equipment in self.equipment_list:
            if equipment.available:
                status = "Available"
            else:
                status = "Rented"

            print(
                equipment.equipment_id,
                "|",
                equipment.name,
                "|",
                equipment.equipment_type,
                "| ₹" + str(equipment.daily_rate),
                "|",
                status
            )
    def rent_equipment(self, equipment_id):
        for equipment in self.equipment_list:

            if equipment.equipment_id == equipment_id:

                if equipment.available:
                    equipment.available = False
                    update_equipment_availability(
                           equipment.equipment_id,False ) 
                    print(equipment.name, "has been rented.")

                    return
                else:
                    print(equipment.name, "is already rented.")
                    return

        print("Equipment not found.")


    def return_equipment(self, equipment_id):
        for equipment in self.equipment_list:

            if equipment.equipment_id == equipment_id:

                if not equipment.available:
                    equipment.available = True

                    update_equipment_availability(
                        equipment.equipment_id,
                        True
                    )

                    print(equipment.name, "has been returned.")
                    return
                else:
                    print(equipment.name, "is already available.")
                    return

        print("Equipment not found.")