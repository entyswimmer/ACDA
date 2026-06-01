import yaml
from models.device import DeviceModel, MosParameters


class ModelLoader:

    @staticmethod
    def load(filepath: str) -> DeviceModel:

        with open(filepath, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        nmos = MosParameters(
            vto=data["nmos"]["vto"],
            gamma=data["nmos"]["gamma"],
            phi=data["nmos"]["phi"],
            nsub=data["nmos"]["nsub"],
            ld=data["nmos"]["ld"],
            uo=data["nmos"]["uo"],
            lambda_=data["nmos"]["lambda"],
            tox=data["nmos"]["tox"],
            pb=data["nmos"]["pb"],
            cj=data["nmos"]["cj"],
            cjsw=data["nmos"]["cjsw"],
            mj=data["nmos"]["mj"],
            mjsw=data["nmos"]["mjsw"],
            cgdo=data["nmos"]["cgdo"],
            js=data["nmos"]["js"],
        )

        pmos = MosParameters(
            vto=data["pmos"]["vto"],
            gamma=data["pmos"]["gamma"],
            phi=data["pmos"]["phi"],
            nsub=data["pmos"]["nsub"],
            ld=data["pmos"]["ld"],
            uo=data["pmos"]["uo"],
            lambda_=data["pmos"]["lambda"],
            tox=data["pmos"]["tox"],
            pb=data["pmos"]["pb"],
            cj=data["pmos"]["cj"],
            cjsw=data["pmos"]["cjsw"],
            mj=data["pmos"]["mj"],
            mjsw=data["pmos"]["mjsw"],
            cgdo=data["pmos"]["cgdo"],
            js=data["pmos"]["js"],
        )

        return DeviceModel(
            nmos=nmos,
            pmos=pmos,
        )