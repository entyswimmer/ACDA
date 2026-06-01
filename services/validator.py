import re


class Validator:

    # -------------------------
    # 入力チェック
    # -------------------------
    def validate_required(self, meta, inputs):

        for inp in meta["inputs"]:
            name = inp["name"]

            if name not in inputs:
                raise ValueError(f"Missing input: {name}")


    # -------------------------
    # 数値チェック
    # -------------------------
    def validate_numeric(self, inputs):

        for k, v in inputs.items():
            try:
                float(v)
            except (TypeError, ValueError):
                raise ValueError(f"{k} is not numeric: {v}")


    # -------------------------
    # 物理チェック
    # -------------------------
    def validate_physics(self, formula_key: str, inputs: dict):

        def must_positive(keys):
            for k in keys:
                if float(inputs[k]) <= 0:
                    raise ValueError(f"{k} must be > 0")

        if formula_key in ["id", "beta", "gm", "ro"]:
            must_positive(inputs.keys())

        if "vov" in inputs and float(inputs["vov"]) <= 0:
            raise ValueError("Vov must be > 0")

        if "vgs" in inputs and "vth" in inputs:
            if float(inputs["vgs"]) < float(inputs["vth"]):
                raise ValueError("Vgs must be >= Vth")


    # -------------------------
    # Expression安全チェック
    # -------------------------
    def validate_expression(self, expr: str):

        forbidden = ["import", "__", "eval", "exec"]

        for f in forbidden:
            if f in expr:
                raise ValueError("Unsafe expression detected")