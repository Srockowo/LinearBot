import args 
import json

with open('config.json', 'r') as config:
    prefix = json.load(config)["prefix"]

def parseInput(text: str):
    defaultArgs = args.default()

    inputList = text.split(' ')
    if inputList[0].startswith(prefix):
        inputList.pop(0)

    for arg in inputList:
        key, value = arg.split('=')

        if key in defaultArgs:
            defaultArgs[key]["value"] = value

    return args.convert(defaultArgs)