import math as Math
import movement

def px(x):
    return x * (1/16)

def closestDistance(z):
    pixels = Math.floor(z / px(1))

    return {
        "pixels": pixels,
        "distance": px(pixels)
    }

def possibilities(vz, strafe45 = False, minDistance = 0.01, prevSlip = 0.6, currSlip = 0.6):
    results = []

    for airtime in range(2,255):
        functions = []
        speed = vz
        zPos = vz
        slip = prevSlip

        for _ in range(airtime):
            if strafe45: functions.append(movement.sprintAir45)
            else: functions.append(movement.sprintAir)

        speed = movement.sprintjump(speed, slip, currSlip)
        slip = currSlip

        for func in functions:
            zPos += speed
            speed = func(speed, slip)
            slip = 1

        results.append({
            "airtime": airtime + 1,
            "distance": zPos + 0.6
        })

    newResults = []

    for result in results:
        closest = closestDistance(result["distance"])
        possBy = result["distance"] - closest["distance"]

        if possBy < minDistance:
            newResults.append({
                "possBy": possBy,
                "closestPixels": closest["pixels"],
                "closestDistance": closest["distance"],
                "airtime": result["airtime"],
                "distance": result["distance"]
            })
    
    return newResults
