# ------------------------------------------------------------
# Audio service setup for piPod
# ------------------------------------------------------------
# piPod uses MPD as the audio backend and sends audio directly
# to the I2S DAC. PipeWire/WirePlumber can grab the ALSA device
# first, causing MPD errors like:
#
#   Failed to open ALSA device "hw:1,0": Device or resource busy
#
# Disable PipeWire for the pi user so MPD can own the DAC.
# ------------------------------------------------------------

echo "Disabling PipeWire/WirePlumber user audio services..."

systemctl --user disable pipewire pipewire-pulse wireplumber 2>/dev/null || true
systemctl --user mask pipewire pipewire-pulse wireplumber 2>/dev/null || true

echo "Enabling MPD system service..."

sudo systemctl enable mpd
