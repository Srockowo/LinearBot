def default():
    return {
        "strafe45": {
            "value": "False",
            "type": parseBoolArg,
            "description": "Whether the simulation will be done with a sprintjump45 or a sprintjump."
        },
        "mindistance": {
            "value": 0.01,
            "type": float,
            "description": "The amount a jump should be possible by to be included in results."
        },
        "airtime": {
            "value": 2,
            "type": parseIntArg,
            "description": "Starting airtime for the simulation. Accepts values between 0 and 255."
        },
        "speed": {
            "value": 0,
            "type": float,
            "description": "The initial speed."
        },
        "prevslip": {
            "value": 0.6,
            "type": float,
            "description": "Slip of the previous tick."
        },
        "currentslip": {
            "value": 0.6,
            "type": float,
            "description": "Slip of the sprintjump tick."
        },
        "results": {
            "value": 25,
            "type": int,
            "description": "The amount of results to display. By default, this exceeds message character limit."
        },
    }

def parseBoolArg(val: str):
    return val.lower() in ["true", "yes", "t", "y"]

def parseIntArg(val: str):
    return int(float(val))

def convert(args: dict[str, dict[str, any]]):
    for key, value in args.items():
        args[key] = value["type"](value["value"])

    return args