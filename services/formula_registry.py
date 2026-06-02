from formulas.mos_basic import (
    cal_cox,
    cal_uCox,
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
                "category": "MOS",
                "device_select": True,
                "function": cal_cox,
                "inputs": [
                    {
                        "name": "tox",
                        "source": "tox",
                        "editable": True
                    }
                ],
                "unit": "F/cm²"
            },

            "ucox": {
                "name": "μCox",
                "category": "MOS",
                "device_select": True,
                "function": cal_uCox,
                "inputs": [
                    {
                        "name": "u",
                        "source": "uo",
                        "editable": True
                    },
                    {
                        "name": "cox",
                        "source": "cox",
                        "editable": True
                    }
                ],
                "unit": "A/V²"
            },

            "beta": {
                "name": "β",
                "category": "MOS",
                "device_select": True,
                "function": cal_beta,
                "inputs": [
                    {
                        "name": "ucox",
                        "source": "ucox",
                        "editable": True
                    },
                    {
                        "name": "w"
                    },
                    {
                        "name": "l"
                    }
                ],
                "unit": "A/V²"
            },

            "delta_ov": {
                "name": "ΔVov",
                "category": "MOS",
                "device_select": True,
                "function": cal_delta_ov,
                "inputs": [
                    {
                        "name": "vgs"
                    },
                    {
                        "name": "vth"
                    }
                ],
                "unit": "V"
            },

            "vov": {
                "name": "Vov",
                "category": "MOS",
                "device_select": True,
                "function": cal_vov,
                "inputs": [
                    {
                        "name": "id"
                    },
                    {
                        "name": "beta"
                    }
                ],
                "unit": "V"
            },

            "id": {
                "name": "Drain Current",
                "category": "MOS",
                "device_select": True,
                "function": cal_id,
                "inputs": [
                    {
                        "name": "w"
                    },
                    {
                        "name": "l"
                    },
                    {
                        "name": "ucox",
                        "source": "ucox",
                        "editable": True
                    },
                    {
                        "name": "vgs"
                    },
                    {
                        "name": "vds"
                    },
                    {
                        "name": "vth"
                    }
                ],
                "unit": "A"
            },

            "gm": {
                "name": "gm",
                "category": "MOS",
                "device_select": True,
                "function": cal_gm,
                "inputs": [
                    {
                        "name": "id"
                    },
                    {
                        "name": "vov"
                    }
                ],
                "unit": "S"
            },

            "ro": {
                "name": "ro",
                "category": "MOS",
                "device_select": True,
                "function": cal_ro,
                "inputs": [
                    {
                        "name": "lammda_",
                        "source": "lambda",
                        "editable": True
                    },
                    {
                        "name": "id"
                    }
                ],
                "unit": "Ω"
            },

            "vth": {
                "name": "Vth",
                "category": "MOS",
                "device_select": True,
                "function": cal_vth,
                "inputs": [
                    {
                        "name": "vtho",
                        "source": "vto",
                        "editable": True
                    },
                    {
                        "name": "gamma",
                        "source": "gamma",
                        "editable": True
                    },
                    {
                        "name": "phi",
                        "source": "phi",
                        "editable": True
                    },
                    {
                        "name": "vsb"
                    }
                ],
                "unit": "V"
            },

            "vgs": {
                "name": "Vgs",
                "category": "MOS",
                "device_select": True,
                "function": cal_vgs,
                "inputs": [
                    {
                        "name": "vth"
                    },
                    {
                        "name": "vov"
                    }
                ],
                "unit": "V"
            },

            "aspect": {
                "name": "W/L",
                "category": "MOS",
                "device_select": True,
                "function": cal_aspect,
                "inputs": [
                    {
                        "name": "id"
                    },
                    {
                        "name": "ucox",
                        "source": "ucox",
                        "editable": True
                    },
                    {
                        "name": "vov"
                    }
                ],
                "unit": "-"
            },

            "parallel": {
                "name": "Parallel Resistance",
                "category": "Passive",
                "device_select": False,
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

    def list_by_category(self):

        result = {}

        for key, formula in self._formulas.items():

            category = formula["category"]

            if category not in result:
                result[category] = []

            result[category].append(key)

        return result