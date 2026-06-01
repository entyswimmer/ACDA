from formulas.mos_basic import (
    cal_cox,
    cal_beta,
    cal_delta_ov,
    cal_vov,
    cal_id,
    cal_gm,
    cal_ro,
    cal_vth,
    cal_vgs,
    cal_aspect
)

from formulas.passive import (
    parallel
)

class FormulaRegistry:

    def __init__(self):

        self._formulas = {

            "cox": {
                "name": "Cox",
                "function": cal_cox,
                "inputs": [
                    "tox",
                    "eps_ox"
                ],
                "unit": "F/cm²"
            },

            "beta": {
                "name": "β",
                "function": cal_beta,
                "inputs": [
                    "mu",
                    "cox",
                    "w",
                    "l"
                ],
                "unit": "A/V²"
            },

            "delta_ov": {
                "name": "ΔVov",
                "function": cal_delta_ov,
                "inputs": [
                    "vgs",
                    "vth"
                ],
                "unit": "V"
            },

            "vov": {
                "name": "Vov",
                "function": cal_vov,
                "inputs": [
                    "id",
                    "beta"
                ],
                "unit": "V"
            },

            "id": {
                "name": "Drain Current",
                "function": cal_id,
                "inputs": [
                    "beta",
                    "vgs",
                    "vds",
                    "vth"
                ],
                "unit": "A"
            },

            "gm": {
                "name": "gm",
                "function": cal_gm,
                "inputs": [
                    "id",
                    "vov"
                ],
                "unit": "S"
            },

            "ro": {
                "name": "ro",
                "function": cal_ro,
                "inputs": [
                    "lambda_",
                    "id"
                ],
                "unit": "Ω"
            },

            "vth": {
                "name": "Vth",
                "function": cal_vth,
                "inputs": [
                    "vtho",
                    "gamma",
                    "phi",
                    "vsb"
                ],
                "unit": "V"
            },

            "vgs": {
                "name": "Vgs",
                "function": cal_vgs,
                "inputs": [
                    "vth",
                    "vov"
                ],
                "unit": "V"
            },

            "aspect": {
                "name": "W/L",
                "function": cal_aspect,
                "inputs": [
                    "id",
                    "mu",
                    "cox",
                    "vov"
                ],
                "unit": "-"
            },

            "parallel": {
                "name": "parallel_res",
                "function": parallel,
                "inputs": [
                    {
                        "name": "resistors",
                        "type": "variadic"
                    } 
                ],
                "unit": "Ω"
            }
        }

    def get(self, key: str):

        return self._formulas[key]

    def list_keys(self):

        return list(self._formulas.keys())

    def list_names(self):

        return [
            formula["name"]
            for formula in self._formulas.values()
        ]