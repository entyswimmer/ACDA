import numpy as np

# Cox
def cal_cox(tox: float) -> float:
    """
    return F/m2
    """
    eps_ox = 3.9 * 8.854e-16
    return eps_ox / tox

# ベータ
def cal_beta(mu: float, cox: float, w: float, l: float) -> float:
    return mu * cox * (w / l)

# 飽和電圧
def cal_delta_ov(vgs: float, vth: float) -> float:
    return vgs - vth

# オーバードライブ電圧
def cal_vov(id: float, beta: float) -> float:
    return np.sqrt(2 * id / beta)

# ドレイン電流
def cal_id(beta: float, vgs: float, vds: float, vth: float) -> float:
    if vgs > vth and vgs - vth <= vds:
        return beta * (vgs - vth)**2 / 2
    elif vgs > vth and (vgs - vth) > vds:
        return beta * ((vgs - vth) * vds - vds**2 / 2)
    else:
        return 0

# 相互コンダクタンス
def cal_gm(id: float, vov: float) -> float:
    return 2 * id / vov

# 出力抵抗
def cal_ro(lammda_: float, id: float) -> float:
    return 1 / (lammda_*id)

# 基盤バイアス効果
def cal_vth(vtho: float, gamma: float, phi: float, vsb: float) -> float:
    return vtho + gamma*(np.sqrt(np.abs(phi+vsb)) - np.sqrt(np.abs(phi)))

# Vgs
def cal_vgs(vth: float, vov: float) -> float:
    return vth + vov

# アスペクト比
def cal_aspect(id: float, mu: float, cox: float, vov: float) -> float:
    return 2 * id / (mu * cox * vov**2)

