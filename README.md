<h1 align="center">bbk3-gamepad</h3>

## About the project

The "bébé keycube" (BBK3) is a controller-like device that can be used for multiple usages. it is a smaller version of the keycube so it possess less keys but it is easier to handle. In this project it can be used as a gamepad to play some games. The chip inside the BBK3 is a XIAO nRF52840 Sense. It uses the chip's motion sensors as joystick inputs.
## Installation

There shouldn't be anything you need to download to use the BBK3. If you want to edit the code, you'll need either the [arduino IDE](https://www.arduino.cc/) if you edit the C++ version or [python](https://www.python.org/downloads/) with a python IDE (I recommend [MU editor](https://codewith.mu/)) if you edit the python version.

## Usages

You can use the gamepad in games. The BBK3 has mostly been tested through unity. The C++ version needed a custom layout to work properly so it may need some kind of accomodation in other game engines too. <br/>
<br/>
You can use the gyroscope's and accelerometer's inputs to control an object's position and rotation, for example, in the unity project in this repository, you can see a cube. It's rotation is controlled by the gyroscope's inputs.
