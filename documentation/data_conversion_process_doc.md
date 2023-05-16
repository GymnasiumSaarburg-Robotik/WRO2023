# Data conversion

Description of the process to turn raw camera data into usable ball position information


Example data:
`[175, 193, 33, 42, 82, 7, 1, 0, 252, 0, 191, 0, 36, 0, 29, 0, 0, 0, 2, 255]
[1, 0, 118, 0, 165, 0, 28, 0, 24, 0, 0, 0, 3, 255]
[1, 0, 6, 0, 22, 0, 12, 0, 18, 0, 0, 0, 200, 255]`

Following the pixy protocol documentation this raw data can easily be converted into a bitmap
where the 1's represent a block being present at that position and 0's representing areas where
no block is present. Areas of 1's in this bitmap can then be drived towards
as there is a target.

## Problems with this approach
If any target in this bitmap would be directly approached, moving targets
would be approached at their starting position and missed. \
Flickering targets e.g. colored areas that get detected only one in 20 frames
would also be approached resulting in wasted movement

Both constants can be pretty easily understood by using the following graphic:
<img src="https://i.imgur.com/gJ5SAAw.png">

As seen:
The Camera width describes the maximum range of absolute directions the camera captures.
The offsetAngle describes the offset the cam is orientated to the enemy team.

With these constants you can determine the direction a ball is positioned in by using its
position on the x-Axis `x`, the x-Maximum of the cam `xMax`, the cameraWidth `camWdth` and the offsetAngle `offsAngle`

Absolute direction:
`offsAngle + ((x / xMax) * camWdth)`

#Potential risks:
###Risk of surpassing 359°
Example:\
offsAngle = 200°\
x = 1750\
xMax = 2000\
camWdth = 250°\
-> Direction would be 418,75°. If 359° is surpassed, an additional - 359° offset has to be added. 
