# Data decryption

As described in the pixy porting guide the data from the Pixy BUS packet response can be interpreted after the following scheme

Example data:
`[175, 193, 33, 42, 82, 7, 1, 0, 252, 0, 191, 0, 36, 0, 29, 0, 0, 0, 2, 255]
[1, 0, 118, 0, 165, 0, 28, 0, 24, 0, 0, 0, 3, 255]
[1, 0, 6, 0, 22, 0, 12, 0, 18, 0, 0, 0, 200, 255]`

Blocks are converted into absolute directions using two important constants:
#### CameraWidth
#### EnemyDirection / OffsetAngle

Both constants can be pretty easily understood by using the following grahic:
<img src="https://i.imgur.com/gJ5SAAw.png">

As seen:
The Camera width describes the maximum range of absolute directions the camera captures.
The offsetAngle describes the offset the cam is orientated to the enemy team.

With these constants you can determine the direction a ball is positioned in by using its
position on the x-Axis `x`, the x-Maximum of the cam `xMax`, the cameraWidth `camWdth` and the offsetAngle `offsAngle`

Absolute direction:
`offsAngle + ((x / xMax) * camWdth)`

Potential risks:
###Risk of surpassing 359°
Example:\
offsAngle = 200°\
x = 1750\
xMax = 2000\
camWdth = 250°\
-> Direction would be 418,75°. If 359° is surpassed, an additional - 359° offset has to be added. 
