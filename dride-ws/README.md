[![Build Status](https://travis-ci.org/dride/dride-ws.svg?branch=master)](https://travis-ci.org/dride/dride-ws)
[![npm version](https://badge.fury.io/js/dride-ws.svg)](https://badge.fury.io/js/dride-ws)

# dride-ws

This repository is used for the on board Node server. It is a submodule of [dride-core](https://github.com/dride/dride-core)

# Api reference

---

# ADAS

###getRoad()

###### Return: [(int x1,int y1), (int x2,int y2), (int x3,int y3), (int x4,int y4)]

Represent the left roadn lane a line from x1,y1 to x2,y2 and x3,y3 to x4,y4 correspondly

###getFrontCar()

###### Return: [(int x1,int y1), (int x2,int y2)]

Represent a line from the left corner of the object to the right

###roadAngle()

###### Return: int angle

A number between 0-360 that represent the road angle.

###getSpeed()

###### Return: int speed

A number between 0-250 that represent the current speed.

###getCurrenPosition()

###### Return: (real lat, real lon)

A point that represent the current latitude and longitude.

---

# Speech

###startDictation()

###### Return: (string text)

Represent the text that was converted from the voice

###say(string text, string langCode)

###### Return: ()

Will speak the text

---

# DVR

###getVideo(timestamp fromTime, timestamp toTime)

###### Return: (string videoUrl)

The url for the video requested

---

git submodule update --remote --merge
