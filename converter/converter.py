class Converter:
    def convert(self, from_value, to_value, amount):
        if (from_value==0):
            raise ValueError("From value must not be zero.")
        return to_value/from_value*float(amount)*-1