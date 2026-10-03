class Equipment:
    def __init__(self, equipment_id, name, equipment_type, daily_rate):
        self.equipment_id = equipment_id
        self.name = name
        self.equipment_type = equipment_type
        self.daily_rate = daily_rate
        self.available = True