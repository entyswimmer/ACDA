class FormulaExecutor:

    def call(self, meta, inputs):

        func = meta["function"]

        input_meta = meta["inputs"][0]

        if input_meta["type"] == "variadic":
            return func(*inputs["resistors"])

        return func(**inputs)
        