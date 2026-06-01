from sympy import sympify
import numpy as np
import re


ALLOWED_NAMES = {
    "sqrt": np.sqrt,
    "exp": np.exp,
    "log": np.log,
    "pi": np.pi,
}


class Parser:

    def parse(self, expr: str) -> float:
        expr = self._preprocess(expr)
        result = sympify(expr, locals=ALLOWED_NAMES)
        return float(result)


    def _preprocess(self, expr: str) -> str:
        expr = expr.replace(" ", "")

        expr = expr.replace("u", "*1e-6")
        expr = expr.replace("n", "*1e-9")
        expr = expr.replace("k", "*1e3")
        expr = expr.replace("M", "*1e6")

        # 省略記号対策
        expr = expr.replace("^", "**")
        expr = re.sub(r"(\d)\(", r"\1*(", expr)
        expr = expr.replace(")(", ")*(")

        return expr