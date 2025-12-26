class Procedure:
    def __init__(self, procedure_id, name, category, duration_minutes, price_min, price_max):
        self.procedure_id = procedure_id
        self.name = name
        self.category = category
        self.duration_minutes = duration_minutes
        self.price_min = price_min
        self.price_max = price_max

    def __repr__(self):
        return f"Procedure(id={self.procedure_id}, name='{self.name}', category='{self.category}')"

    def get_price_range(self):
        """Get formatted price range"""
        return f"{self.price_min:.0f} - {self.price_max:.0f} RON"

    def get_duration_formatted(self):
        """Get formatted duration"""
        hours = self.duration_minutes // 60
        minutes = self.duration_minutes % 60
        if hours > 0:
            return f"{hours}h {minutes}min"
        else:
            return f"{minutes}min"

    def get_average_price(self):
        """Get average price"""
        return (self.price_min + self.price_max) / 2