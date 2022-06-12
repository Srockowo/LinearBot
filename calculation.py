import math as Math
import movement

def px(x):
    return x / 16

def closestDistance(z):
    pixels = Math.floor(z / px(1))

    return {
        "pixels": pixels,
        "distance": px(pixels)
    }

def possibilities(args: dict):
    results = []

    for airtime in range(args["airtime"],256):
        functions = []
        simArgs = args.copy()
        simArgs["z"] = simArgs["speed"]

        for _ in range(airtime):
            if simArgs["strafe45"]: functions.append(movement.sprintAir45)
            else: functions.append(movement.sprintAir)

        simArgs["speed"] = movement.sprintjump(simArgs["speed"], simArgs["prevslip"], args["currentslip"])
        simArgs["prevslip"] = args["currentslip"]

        for func in functions:
            simArgs["z"] += simArgs["speed"]
            simArgs["speed"] = func(simArgs["speed"], simArgs["prevslip"])
            simArgs["prevslip"] = 1

        results.append({
            "airtime": airtime + 1,
            "distance": simArgs["z"] + 0.6
        })

    newResults = []

    for result in results:
        closest = closestDistance(result["distance"])
        possBy = result["distance"] - closest["distance"]

        if possBy < args["mindistance"]:
            newResults.append({
                "possBy": possBy,
                "closestPixels": closest["pixels"],
                "closestDistance": closest["distance"],
                "airtime": result["airtime"],
                "distance": result["distance"]
            })
    
    return newResults

def toString(results: list[dict], args: dict):
    lengthErrorMsg = "\nMessage exceeded 2000 characters."
    resultMessage = "```\n"

    for index, result in enumerate(results):
        if index >= float(args["results"]): break

        newLine = f"[Poss by: {result['possBy']} {result['closestPixels']}px ({result['closestDistance']} b) "
        newLine += f"Tier {12 - result['airtime']} (Airtime {result['airtime']}) Distance: {result['distance']}]\n"

        if (len(resultMessage + newLine) >= 1999 - len(lengthErrorMsg)):
            resultMessage += lengthErrorMsg
            break
        else: resultMessage += newLine

    return resultMessage + "\n```"