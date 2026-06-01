class UnitConverter:

    PREFIX = {
        "p": 1e-12,
        "n": 1e-9,
        "u": 1e-6,
        "m": 1e-3,
        "k": 1e3,
        "M": 1e6,
    }

    def convert(self, value: str) -> float:
        for k, v in self.PREFIX.items():
            if value.endswith(k):
                return float(value[:-1]) * v
        return float(value)