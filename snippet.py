#!/usr/bin/env python

import base64
import json

colours = [01, 19, 40, 50, 60, 70, 80, 90]

def toJson(colour, channel):
    if channel < 1 or channel > 9:
        return
    channel = channel - 1
    hexs = "00 00 00 00 00 00 00 00 00"
    data = bytearray.fromhex(hexs)
    data[channel] = colours[colour]
    channelData = base64.b64encode(data)
    jsonData ="{'id'[1],'data':'" + channelData + "'}"
    return json.dumps(jsonData)

result = toJson(0,1)
if not result:
    print("no result")
else:
    print(result)
