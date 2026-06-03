class UnitConverter:

    PREFIX = {
        "p": 1e-12,
        "n": 1e-9,
        "u": 1e-6,
        "m": 1e-3,
        "k": 1e3,
        "M": 1e6,
    }

    PREFIX_ORDER = [
        ("M", 1e6),
        ("k", 1e3),
        ("", 1.0),
        ("m", 1e-3),
        ("u", 1e-6),
        ("n", 1e-9),
        ("p", 1e-12),
    ]

    def convert(self, value: str) -> float:
        for k, v in self.PREFIX.items():
            if value.endswith(k):
                return float(value[:-1]) * v
        return float(value)

    def format_value(
        self,
        value: float,
        decimals: int = 3,
    ) -> str:

        number = float(value)

        if number == 0:
            return "0"

        sign = "-" if number < 0 else ""
        abs_val = abs(number)

        symbol, scaled = self._best_prefix(abs_val)

        text = (
            f"{scaled:.{decimals}f}"
            .rstrip("0")
            .rstrip(".")
        )

        return f"{sign}{text}{symbol}"

    def _best_prefix(
        self,
        abs_val: float,
    ) -> tuple[str, float]:

        for symbol, scale in self.PREFIX_ORDER:
            scaled = abs_val / scale

            if 1 <= scaled < 1000:
                return symbol, scaled

        for symbol, scale in reversed(
            self.PREFIX_ORDER
        ):
            scaled = abs_val / scale

            if 0.001 <= scaled < 1:
                return symbol, scaled

        symbol, scale = self.PREFIX_ORDER[0]

        return symbol, abs_val / scale