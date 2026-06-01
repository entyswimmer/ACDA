class VariableStore:

    def __init__(self):
        self._vars = {}

    def set(self, name: str, value: float):
        self._vars[name] = value

    def get_all(self):
        return self._vars