# HiTechnic (NXT) Compass Sensor

## General Info

|                 |                                                                                                                     |
|-----------------|---------------------------------------------------------------------------------------------------------------------|
| Driver Name     | `ht-nxt-compass `                                                                                                   |
| Website         | [*Klick\*](https://modernroboticsinc.com/product-category/hitechnic/cgi-bin/commerce.cgi?preadd=action&key=NMC1034) |
| Connection Type | NXT/I2C                                                                                                             |
| Default Address | 0x01                                                                                                                |
| Vendor ID       | `HITECHNC`/`HiTechnc`                                                                                               |
| Product ID      | `Compass`                                                                                                           |
| Number of Modes | 1                                                                                                                   |


## Modes

| Mode      | Description       | Units | Decimals | Num. Values | Values                         |
|-----------|-------------------|-------|----------|-------------|--------------------------------|
| `COMPASS` | Compass Direction | deg   | 0        | 1           | `value0`: Direction (0 to 359) |      

## Commands

| Command     | Description       |
|-------------|-------------------|
| `BEGIN-CAL` | Begin calibration |
| `END-CAL`   | End calibration   |

## Snippet

`compass = Ev3devSensor(Port.S1)`\
`direction = compass.read("COMPASS")[0]`
