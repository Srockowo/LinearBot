import args 

def parseInput(text: str):
    defaultArgs = args.default()

    for arg in text.split(' '):
        key, value = arg.split('=')

        if key in defaultArgs:
            defaultArgs[key]["value"] = value

    return args.convert(defaultArgs)