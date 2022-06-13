# Exercise: discovery of RSSI measurements

This work is based on the code provided in the repository. Portions of code are missing, that you must complete to achieve the goals assigned to you.

## Introduction

You are provided with a CSV file containing calibration data for a positioning system. The calibration was performed in the Numerica building (Montbéliard university site, FEMTO-ST offices) by walking from calibration point to calibration point. At each of these points, we stopped, faced north and triggered a measurements (several seconds), then repeated this process facing east, then south, then west. Then, we went to the next point and repeated the 4 measurements.

Each line of the file is structured as follows:

* First field: x coordinate of the calibration point
* Second field: y coordinate of the calibration point
* Third field: z coordinate of the calibration point
* Fourth field: mobile device orientation, with 4 values possible:
	* 1: facing north
	* 2: facing east
	* 3: facing south
	* 4: facing west
* Remaining fields as pairs (so, the count of remaining fields is even):
	* First field of a pair: Source MAC address of the frame whose RSSI is measured during calibration (as 6 groups of hexadecimal digits separated by ':')
	* Second field of a pair: RSSI or the frame, as measured during the calibration process

## Instructions

In this exercise, you have to import RSSI data from the CSV file and aggregate RSSI for duplicate MAC addresses values. The aggregated value must be the average value of the signals received for a given location. Since the dBm scale is not linear (it is logarithmic), you have to convert the RSSI's to their mW value, compute their average values, then convert the result back to dBm.

Here are the formulas to convert between both units and scales:

* From mW to dBm: P(dBm) = 10.0 log (P(mW))
* From dBm to mW: P(mW) = 10.0 ^ (P(dBm)/10.0)

The content of the file must be loaded into memory with the values for identical MAC addresses aggregated by lines. Then you must output the resulting structured data into a CSV file named 'result.csv', with 1 line for each point (also collapse the orientations, i.e. you must merge the 4 corresponding lines of a given x,y,z location, and put its orientation to zero). Therefore, each line of the resulting file must ensure the following properties:

* Its x,y,z set of values is unique
* Its orientation value is 0
* Its pairs of RSSI samples (defined by a MAC address and its associated RSSI) are ordered by MAC addresses (ascending order)
