def sprintjump(vz, prevSlip, currSlip):
    return vz * prevSlip * 0.91 + 0.1 * 1.274 * 1 * (0.6 / currSlip) ** 3 + 0.2

def sprintAir(vz, prevSlip):
    return vz * prevSlip * 0.91 + 0.02 * 1.274

def sprintAir45(vz, prevSlip):
    return vz * prevSlip * 0.91 + 0.02 * 1.3