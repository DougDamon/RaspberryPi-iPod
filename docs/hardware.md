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
	+ Button 1: GPIO 16
	+ Button 2: GPIO 22
	+ Button 3: GPIO 23
	+ Button 4: GPIO 27
	+ Volume Up: GPIO 20
	+ Volume Down: GPIO 26
- Future mapping ideas:
- Notes:  May consider dedicated volume buttons or possibly a small rotary controller on the side of the device.  These buttons will increase/decrease volume regardless of where the user is in the device interface.

## Audio Output

- Audio interface: I2S
- DAC: PCM5102A I2S DAC breakout
- Headphone amplifier: Electrodragon TPA6132 breakout
- Headphone output: confirmed working
- Speaker output: not currently implemented

### Raspberry Pi to PCM5102A

- BCK: GPIO18 / physical pin 12
- DIN: GPIO21 / physical pin 40
- LRCLK/LRCK/LCK: GPIO19 / physical pin 35
- GND: physical pin 6 or 14
- VCC: regulated 5 V from physical pin 2 or 4

### PCM5102A Configuration

- PCM5102A SCK pin is connected to ground.
- The PCM5102A breakout provides single-ended analog outputs:
  - Left
  - Right
  - Ground
- The PCM5102A is configured using the `hifiberry-dac` device-tree overlay.

### TPA6132 Headphone Amplifier

- Supply: regulated 5 V
- Gain: fixed at -6 dB
- Breakout gain configuration:
  - R2 populated
  - R4 populated
- Audio connections:
  - PCM left output -> TPA L+
  - PCM right output -> TPA R+
  - PCM audio ground -> TPA L-
  - PCM audio ground -> TPA R-
  - System/audio ground -> TPA power GND
- Headphone connections:
  - TPA L -> headphone jack tip
  - TPA R -> headphone jack ring
  - TPA G -> headphone jack sleeve
- DET is Active Low connected to GPIO 24
- Audio transition testing:
  - Play/pause: clean
  - Track changes: clean
  - Power-down: clean
  - Idle noise: no audible hiss or hum
  - Power-up: essentially clean; a very faint intermittent startup tick may be present
- No additional analog muting or pop-suppression circuitry is currently required.
- 
### Notes

- The PCM5102A and TPA6132 share the same regulated 5 V supply and common ground.
- The TPA6132 operated correctly during breadboard testing at -6 dB gain.
- At -6 dB, 60% MPD software volume was already louder than comfortable with the test headphones.
- Smaller software-volume increments will be needed, but this is a software configuration issue rather than a hardware change.
- Confirm whether the TPA6132 breakout already contains input coupling capacitors before reproducing the amplifier circuit or breakout connections on a custom PCB.
- Test for hiss, display-related noise, startup/shutdown pops, and breadboard connection sensitivity before finalizing the perfboard layout.
- The tutorial labels the I2S word-select signal `LCK`; other Raspberry Pi and I2S references may call the same signal `LRCLK`, `LRCK`, or word clock.
- Reference tutorial: https://www.instructables.com/Raspberry-Pi-HQ-Audio-PCM5102-and-MPD/

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
| Display Buttons | Button 1 | GPIO 16 / Pin 36 | PiTFT | Remapped from GPIO 17 to avoid conflict with the Witty Pi GPIO 17 usage |
| Display Buttons | Button 2 | GPIO 22 / Pin 15 | PiTFT | From PiTFT documentation |
| Display Buttons | Button 3 | GPIO 23 / Pin 16 | PiTFT | From PiTFT documentation |
| Display Buttons | Button 4 | GPIO 27 / Pin 13 | PiTFT | From PiTFT documentation |
| Volume Control | Volume Down | GPIO 26 / Pin 37 | Side button | Global volume control |
| Volume Control | Volume Up | GPIO 20 / Pin 38 | Side button | Global volume control |
| Encoder | I2C SDA | GPIO 2 / Pin 3 | ANO I2C Adapter | Shared I2C bus |
| Encoder | I2C SCL | GPIO 3 / Pin 5 | ANO I2C Adapter | Shared I2C bus |
| Encoder | I2C Address | 0x49 | ANO I2C Adapter | Default address |
| Audio DAC | I2S BCLK | GPIO 18 / Pin 12 | PCM5102 | I2S audio |
| Audio DAC | I2S LRCLK | GPIO 19 / Pin 35 | PCM5102 | I2S audio |
| Audio DAC | I2S DIN | GPIO 21 / Pin 40 | PCM5102 | I2S audio |
| Audio Headphone Amp| DET | GPIO 24 / Pin 18 | TPA6132 | Headphone detection|
| Power | Shutdown sequence | GPIO 4 / Pin 7 | Witty Pi 4 L3V7 | Default shutdown signal pin |
| Power | System state / power monitoring | GPIO 17 / Pin 11 | Witty Pi 4 L3V7 | GPIO 17 reserved for Witty Pi; PiTFT Button 1 remapped |
| Power | Control/status | GPIO 5 / Pin 29 | Witty Pi 4 L3V7 | Used by onboard microcontroller |
| Power | Control/status | GPIO 6 / Pin 31 | Witty Pi 4 L3V7 | Used by onboard microcontroller |
| Power | I2C SDA | GPIO 2 / Pin 3 | Witty Pi 4 L3V7 | Shared I2C bus for RTC / temperature sensor |
| Power | I2C SCL | GPIO 3 / Pin 5 | Witty Pi 4 L3V7 | Shared I2C bus for RTC / temperature sensor |

## Resolved Pin Conflicts

| GPIO / Pin | Original Conflict | Resolution |
|---|---|---|
| GPIO 17 / Pin 11 | PiTFT Button 1 and Witty Pi 4 L3V7 both wanted GPIO 17 | PiTFT Button 1 was remapped to GPIO 16 / Pin 36 |

Notes:
- GPIO 17 is reserved for Witty Pi system state / power management monitoring.
- GPIO 2 and GPIO 3 are shared by the ANO encoder adapter and the Witty Pi 4 L3V7.
- This I2C sharing is expected as long as device addresses do not conflict.

## Known Hardware Issues

- I2C read errors from rotary encoder/seesaw board
- Display refresh/flicker issues, probably software-related but visible on hardware
- Display times out to a white screen; desired behavior is to turn the screen off instead.

## Hardware Validation

- PiTFT Buttons 1–4 tested with a simple `gpiozero` script.
- Button 1 is remapped from GPIO 17 to GPIO 16.
- Side volume buttons tested with `gpiozero`.
- Volume Up uses GPIO 20 / Pin 38.
- Volume Down uses GPIO 26 / Pin 37.

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