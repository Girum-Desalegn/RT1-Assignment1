Assignment_1 Python Robotics Simulator
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
The Research Track I course has seen modifications in certain arenas and assignments. In this particular assignment, the task involves creating a Python node to control a robot, directing it to gather all the golden boxes. The objective is to develop code that consolidates all collected boxes onto a single base box. The assignment code incorporates functions and a while loop to fulfill this specific requirement

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

After setup those requirement you can run the program with:
```python
python2 run.py assignment.py
```

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```
[sr-api]: https://studentrobotics.org/docs/programming/sr/

Pseudocode
---------
Creating pseudocode proves to be a convenient and effective step in preparing for the subsequent coding tasks in this assignment. Below, you'll find the provided pseudocode to facilitate the coding process.
```python
while true:
	if robot want to grab:
		find tokens distance rotation and code
	else:
		find base token distance rotation and code
	if no token detected:
		if all token released:
			exit the program
		else:
			turn round search it 
	else if dist< the threshold of grab and robot want to grab:
		grab token
		save the token code on the list
		robot don't want to grab
	else if dist< the threshold of release and robot don't want to grab:
		release token
		count the of token released
		save the token code on the list
		robot want to grab
	else if robot well aligned:
		go straight
	else if the robot inclined on the left side:
		tun right
	else if the robot inclined on the right side:
		tun left
```
Further improvement 
---------
This task entails the robot initially choosing a box, grasping it, and subsequently collecting the remaining boxes before releasing them in the vicinity. As part of the enhancement, the robot is now tasked with autonomously identifying a specific point within the workspace. Once this designated point is located, the robot is instructed to select a box, securely grasp it, and systematically place it down at the identified point in an organized manner. This refinement in the robot's behavior aims to enhance its precision and contribute to a more methodical execution of tasks within the workspace.
