# 抵抗の並列
def parallel(*resistors: float) -> float:
    return 1/sum(1/r for r in resistors)

#　直列分圧・並列分流
def divider(input_val: float, upper: float, lower: float) -> float:
    return input_val * (lower / (upper + lower))

#　