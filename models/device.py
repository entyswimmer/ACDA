from dataclasses import dataclass

@dataclass
class MosParameters:
    vto: float
    gamma: float
    phi: float
    nsub: float
    ld: float
    uo: float
    lambda_: float
    tox: float
    pb: float
    cj: float
    cjsw: float
    mj: float
    mjsw: float
    cgdo: float
    js: float


@dataclass
class DeviceModel:
    nmos: MosParameters
    pmos: MosParameters