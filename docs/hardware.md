# Hardware Inventory

## Current Prototype

Brief description of the current working hardware prototype.

## Compute

- Raspberry Pi model: Zero 2W
- OS: Debian GNU/Linux 12 (bookworm)
- Power source: 
- Storage: 

## Display

- Display model:Adafruit PiTFT 2.2" HAT Mini Kit - 320x240 2.2" TFT - No Touch (Product ID: 2315)
- Size: 2.2"
- Resolution: 320x240
- Interface:
- Driver/library: fbcp (not sure if this is actually required for this use case)
- GPIO pins used: SCK, MOSI, MISO, CE0, CE1, 25
- Notes: I followed these instructions for installation https://learn.adafruit.com/adafruit-2-2-pitft-hat-320-240-primary-display-for-raspberry-pi/easy-install
	
	Should I also be using pin 24 for reset?  It might be a good idea
	
	Buttons will be covered in the Button section

## Rotary Encoder

- Encoder board/model: ANO Directional Navigation and Scroll Wheel Rotary Encoder (Product ID: 5001) with Adafruit ANO Rotary Navigation Encoder to I2C Stemma QT Adapter (Product ID: 5740)
- Interface:
- I2C address: 0x49 (default)
- Pins/buttons:
- Notes: I followed this tutorial to get started (https://learn.adafruit.com/adafruit-ano-rotary-navigation-encoder-to-i2c-stemma-qt-adapter)

## Buttons

- Number of buttons: 4 (these are the 4 buttongs on the Display)
- Location:
- Connected through:
- Current mapping:
	+ Button 1: GPIO 17
	+ Button 2: GPIO 22
	+ Button 3: GPIO 23
	+ Button 4: GPIO 27
- Future mapping ideas:

## Audio Output

- Current audio output: PCM5102 I2S DAC
- DAC/amp: PCM5102
- Speaker/headphone support: TBD
- Interface: I2S
- GPIO pins used:
  - BCK: GPIO 18 / physical pin 12
  - DIN: GPIO 21 / physical pin 40
  - LCK/LRCLK: GPIO 19 / physical pin 35
  - GND: physical pin 6 or 14
  - VCC: 5V physical pin 2 or 4
- Notes: 
	- SCK is not connected. Tutorial listed SCK as NC / internal via link.
	- Tutorial (https://www.instructables.com/Raspberry-Pi-HQ-Audio-PCM5102-and-MPD/)

## Power

- Current power method: Witty Pi 4 L3V7 - RTC & Power Management for Raspberry Pi (Product ID: 5705)
- Battery support:
- Charging:
- Power switch:
- Notes:

## Wiring

| Subsystem | Signal | GPIO / Pin | Used By | Notes |
|---|---|---:|---|---|
| Display | SPI SCK | GPIO 11 / Pin 23 | PiTFT | Hardware SPI |
| Display | SPI MOSI | GPIO 10 / Pin 19 | PiTFT | Hardware SPI |
| Display | SPI MISO | GPIO 9 / Pin 21 | PiTFT | Listed by Adafruit as used |
| Display | SPI CE0 | GPIO 8 / Pin 24 | PiTFT | Display chip select |
| Display | SPI CE1 | GPIO 7 / Pin 26 | PiTFT | Used by PiTFT |
| Display | GPIO 25 | GPIO 25 / Pin 22 | PiTFT | Used by PiTFT |
| Display Buttons | Button 1 | GPIO #17 | PiTFT | Need confirm exact GPIO |
| Display Buttons | Button 2 | GPIO #22 | PiTFT | Need confirm exact GPIO |
| Display Buttons | Button 3 | GPIO #23 | PiTFT | Need confirm exact GPIO |
| Display Buttons | Button 4 | GPIO #27 | PiTFT | Need confirm exact GPIO |
| Encoder | I2C SDA | GPIO 2 / Pin 3 | ANO I2C Adapter | Shared I2C bus |
| Encoder | I2C SCL | GPIO 3 / Pin 5 | ANO I2C Adapter | Shared I2C bus |
| Encoder | I2C Address | 0x49 | ANO I2C Adapter | Default address |
| Audio DAC | I2S BCLK | GPIO 18 / Pin 12 | PCM5102 | I2S audio |
| Audio DAC | I2S LRCLK | GPIO 19 / Pin 35 | PCM5102 | I2S audio |
| Audio DAC | I2S DIN | GPIO 21 / Pin 40 | PCM5102 | I2S audio |
| Power | Power / RTC / UPS | TBD | Witty Pi 4 L3V7 | Need document occupied pins |

## Known Hardware Issues

- I2C read errors from rotary encoder/seesaw board
- Display refresh/flicker issues, probably software-related but visible on hardware
- Display times out to a white screen.  Need to change the to turning the screen off

## Notes
- All Product IDs refer to Adafruit Product IDs.

## PCB Goals

- Reduce hand wiring
- Make assembly repeatable
- Support current display
- Support rotary encoder and four buttons
- Keep Raspberry Pi Zero 2 W accessible
- Leave room for future power/audio improvements

## Case Goals

- Hold Pi, display, encoder, and buttons securely
- Easy access to USB/power/audio/SD card
- Printable with minimal supports
- Easy to assemble/disassemble 

## Open question:
- Confirm whether the PiTFT reset line should use GPIO 24 or whether the current setup is sufficient without it.