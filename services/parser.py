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

        prefix = {"p": "1e-12", "n": "1e-9", "u": "1e-6", "m": "1e-3", "k": "1e3", "M": "1e6"}
        expr = re.sub(r"(\d+(?:\.\d+)?)([pnumkM])\b", lambda m: f"{m.group(1)}*{prefix[m.group(2)]}", expr)

        # 省略記号対策
        expr = expr.replace("^", "**")
        expr = re.sub(r"(\d)\(", r"\1*(", expr)
        expr = expr.replace(")(", ")*(")

        return expr