import re


class Validator:

    def validate(
        self,
        formula_key: str,
        meta: dict,
        inputs: dict
    ):

        self.validate_required(
            meta,
            inputs
        )

        self.validate_numeric(
            inputs
        )

        self.validate_physics(
            formula_key,
            inputs
        )

    # -------------------------
    # 必須入力チェック
    # -------------------------

    def validate_required(
        self,
        meta,
        inputs
    ):

        for item in meta["inputs"]:

            name = item["name"]

            if name not in inputs:

                raise ValueError(
                    f"Missing input: {name}"
                )

    # -------------------------
    # 数値チェック
    # -------------------------

    def validate_numeric(
        self,
        inputs
    ):

        for key, value in inputs.items():

            if isinstance(
                value,
                list
            ):

                for item in value:

                    try:
                        float(item)

                    except (
                        TypeError,
                        ValueError
                    ):

                        raise ValueError(
                            f"{key} contains non numeric value: {item}"
                        )

            else:

                try:
                    float(value)

                except (
                    TypeError,
                    ValueError
                ):

                    raise ValueError(
                        f"{key} is not numeric: {value}"
                    )

    # -------------------------
    # 物理チェック
    # -------------------------

    def validate_physics(
        self,
        formula_key: str,
        inputs: dict
    ):

        def must_positive(keys):

            for key in keys:

                if key not in inputs:
                    continue

                if float(inputs[key]) <= 0:

                    raise ValueError(
                        f"{key} must be > 0"
                    )

        # β = μCox(W/L)
        if formula_key == "beta":

            must_positive(
                [
                    "ucox",
                    "w",
                    "l"
                ]
            )

        # Id計算
        elif formula_key == "id":

            must_positive(
                [
                    "w",
                    "l",
                    "ucox"
                ]
            )

            if (
                "vgs" in inputs
                and
                "vth" in inputs
            ):

                if (
                    float(inputs["vgs"])
                    <
                    float(inputs["vth"])
                ):

                    raise ValueError(
                        "Vgs must be >= Vth"
                    )

        # gm = 2Id/Vov
        elif formula_key == "gm":

            must_positive(
                [
                    "id",
                    "vov"
                ]
            )

        elif formula_key == "ro":

            must_positive(
                [
                    "lamda_",
                    "id"
                ]
            )
            )

        # Vov
        elif formula_key == "vov":

            must_positive(
                [
                    "id",
                    "beta"
                ]
            )

        # Aspect
        elif formula_key == "aspect":

            must_positive(
                [
                    "id",
                    "ucox",
                    "vov"
                ]
            )

        # Parallel
        elif formula_key == "parallel":

            resistors = inputs.get(
                "resistors",
                []
            )

            if len(resistors) < 2:

                raise ValueError(
                    "At least two resistors are required"
                )

            for r in resistors:

                if float(r) <= 0:

                    raise ValueError(
                        "Resistance must be > 0"
                    )

    # -------------------------
    # Expression安全チェック
    # -------------------------

    def validate_expression(
        self,
        expr: str
    ):

        forbidden_patterns = [
            r"\bimport\b",
            r"__",
            r"\beval\b",
            r"\bexec\b"
        ]

        for pattern in forbidden_patterns:

            if re.search(
                pattern,
                expr
            ):

                raise ValueError(
                    "Unsafe expression detected"
                )