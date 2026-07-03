# Hardware Inventory

## Current Prototype

Working prototype of a Raspberry Pi Zero 2 W portable media player using a 2.2" PiTFT display, ANO rotary encoder, PCM5102 I2S DAC, and Witty Pi 4 L3V7 power-management board.

## Compute

- Raspberry Pi model: Zero 2W
- OS: Debian GNU/Linux 12 (bookworm)
- Power source: 
- Storage: 

## Display

- Display model: Adafruit PiTFT 2.2" HAT Mini Kit - 320x240 2.2" TFT - No Touch (Product ID: 2315)
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

- Number of buttons: 4 (these are the 4 buttons on the Display)
- Location:
- Connected through:
- Current mapping:
	+ Button 1: GPIO 17
	+ Button 2: GPIO 22
	+ Button 3: GPIO 23
	+ Button 4: GPIO 27
- Future mapping ideas:
- Notes:  May consider dedicated volume buttons or possibly a small rotary controller on the side of the device.  These buttons will increase/decrease volume regardless of where the user is in the device interface.

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
	- The PCM5102 tutorial uses `LCK`, while Raspberry Pi / I2S references often call the same signal `LRCLK`, `LRCK`, or word clock.

## Power

- Current power method: Witty Pi 4 L3V7 - RTC & Power Management for Raspberry Pi (Product ID: 5705)
- Battery support:
- Charging:
- Power switch:
- Notes:
  - Provides RTC and power-management functionality.
  - Uses GPIO pins for shutdown, system state monitoring, and control/status signaling.
  - Uses the Raspberry Pi I2C bus for RTC and temperature sensor communication.

## Raspberry Pi Pin Usage

| Subsystem | Signal | GPIO / Pin | Used By | Notes |
|---|---|---:|---|---|
| Display | SPI SCK | GPIO 11 / Pin 23 | PiTFT | Hardware SPI |
| Display | SPI MOSI | GPIO 10 / Pin 19 | PiTFT | Hardware SPI |
| Display | SPI MISO | GPIO 9 / Pin 21 | PiTFT | Listed by Adafruit as used |
| Display | SPI CE0 | GPIO 8 / Pin 24 | PiTFT | Display chip select |
| Display | SPI CE1 | GPIO 7 / Pin 26 | PiTFT | Used by PiTFT |
| Display | GPIO 25 | GPIO 25 / Pin 22 | PiTFT | Used by PiTFT |
| Display Buttons | Button 1 | GPIO 17 / Pin 11 | PiTFT | Conflicts with Witty Pi GPIO 17 usage |
| Display Buttons | Button 2 | GPIO 22 / Pin 15 | PiTFT | From PiTFT documentation |
| Display Buttons | Button 3 | GPIO 23 / Pin 16 | PiTFT | From PiTFT documentation |
| Display Buttons | Button 4 | GPIO 27 / Pin 13 | PiTFT | From PiTFT documentation |
| Volume Control | Volume Down | TBD | Side buttons or side rotary | Future global volume control |
| Volume Control | Volume Up | TBD | Side buttons or side rotary | Future global volume control |
| Encoder | I2C SDA | GPIO 2 / Pin 3 | ANO I2C Adapter | Shared I2C bus |
| Encoder | I2C SCL | GPIO 3 / Pin 5 | ANO I2C Adapter | Shared I2C bus |
| Encoder | I2C Address | 0x49 | ANO I2C Adapter | Default address |
| Audio DAC | I2S BCLK | GPIO 18 / Pin 12 | PCM5102 | I2S audio |
| Audio DAC | I2S LRCLK | GPIO 19 / Pin 35 | PCM5102 | I2S audio |
| Audio DAC | I2S DIN | GPIO 21 / Pin 40 | PCM5102 | I2S audio |
| Power | Shutdown sequence | GPIO 4 / Pin 7 | Witty Pi 4 L3V7 | Default shutdown signal pin |
| Power | System state / power monitoring | GPIO 17 / Pin 11 | Witty Pi 4 L3V7 | Conflicts with PiTFT Button 1 |
| Power | Control/status | GPIO 5 / Pin 29 | Witty Pi 4 L3V7 | Used by onboard microcontroller |
| Power | Control/status | GPIO 6 / Pin 31 | Witty Pi 4 L3V7 | Used by onboard microcontroller |
| Power | I2C SDA | GPIO 2 / Pin 3 | Witty Pi 4 L3V7 | Shared I2C bus for RTC / temperature sensor |
| Power | I2C SCL | GPIO 3 / Pin 5 | Witty Pi 4 L3V7 | Shared I2C bus for RTC / temperature sensor |

## Known Pin Conflicts

| GPIO / Pin | Used By | Conflict |
|---|---|---|
| GPIO 17 / Pin 11 | PiTFT Button 1, Witty Pi 4 L3V7 | PiTFT Button 1 conflicts with Witty Pi system state / power management monitoring |

Notes:
- GPIO 2 and GPIO 3 are shared by the ANO encoder adapter and the Witty Pi 4 L3V7.
- This I2C sharing is expected as long as device addresses do not conflict.
- GPIO 17 must be resolved before PCB design.

## Known Hardware Issues

- I2C read errors from rotary encoder/seesaw board
- Display refresh/flicker issues, probably software-related but visible on hardware
- Display times out to a white screen; desired behavior is to turn the screen off instead.

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
- Roughly the size of a 4th generation iPod

## Case Design Intent

The case is intended to follow the general handheld media-player layout of a 4th generation iPod:

- Display near the top
- Rotary controller / navigation wheel below the display
- Pocketable handheld form factor
- One-handed navigation
- Minimal front-panel controls

The design goal is to preserve the familiar ergonomics of a classic dedicated music player while adapting the layout for Raspberry Pi hardware, a PiTFT display, and the ANO rotary controller.

## Open Questions

- Confirm whether the PiTFT reset line should use GPIO 24 or whether the current setup is sufficient without it.
- Confirm which GPIO/header pins are occupied by the Witty Pi 4 L3V7.
- Confirm battery type/capacity and charging behavior.
- Confirm physical audio output path: headphone jack, line out, amp, or speaker.
- Confirm whether `fbcp` is required for the current pygame display setup.
- Decide how to resolve the GPIO 17 conflict between PiTFT Button 1 and Witty Pi 4 L3V7.