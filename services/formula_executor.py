class FormulaExecutor:

    def call(self, meta, inputs):

        func = meta["function"]

        inputs_meta = meta.get("inputs", [])
        if inputs_meta and isinstance(inputs_meta[0], dict) and inputs_meta[0].get("type") == "variadic":
            variadic_name = inputs_meta[0].get("name")
            return func(*inputs[variadic_name])

        return func(**inputs)
        