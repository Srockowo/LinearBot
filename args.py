def default():
    return {
        "results": {
            "value": 25,
            "type": int
        },
        "speed": {
            "value": 0,
            "type": float
        },
        "strafe45": {
            "value": "false",
            "type": parseBoolArg
        },
        "mindistance": {
            "value": 0.01,
            "type": float
        },
        "prevslip": {
            "value": 0.6,
            "type": float
        },
        "currentslip": {
            "value": 0.6,
            "type": float
        },
        "airtime": {
            "value": 2,
            "type": parseIntArg
        }
    }

def parseBoolArg(val: str):
    return val.lower() in ["true", "yes", "t", "y"]

def parseIntArg(val: str):
    return int(float(val))

def convert(args: dict[str, dict[str, any]]):
    for key, value in args.items():
        args[key] = value["type"](value["value"])

    return args