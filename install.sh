#!/usr/bin/env bash
# ============================================================
#  install.sh
#  Installs all dependencies for:
#    - main light control script (NeoPixel / TSL2591)
#    - visualize.py (pandas / matplotlib)
#    - DHT sensor script (adafruit-circuitpython-dht)
#    - GPIO scripts (rpi-lgpio)
#    - OpenCV scripts (cv2)
#
#  Place this file inside your diel-light-pi/ folder and run:
#    chmod +x install.sh
#    ./install.sh
# ============================================================

set -e  # Exit immediately on error

# ── Colour helpers ────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Colour

info()    { echo -e "${CYAN}[INFO]${NC}  $*"; }
success() { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*"; exit 1; }

# ── 0. Move into the project folder ──────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"
VENV_DIR="$PROJECT_DIR/venv"

info "Project directory: $PROJECT_DIR"
cd "$PROJECT_DIR"

# ── 1. Sanity checks ─────────────────────────────────────────
info "Checking for Python 3..."
python3 --version >/dev/null 2>&1 || error "Python 3 is not installed. Please install it first."
success "Python 3 found: $(python3 --version)"

info "Checking for pip3..."
pip3 --version >/dev/null 2>&1 || error "pip3 is not installed. Run: sudo apt-get install -y python3-pip"
success "pip3 found."

# ── 2. System-level apt packages (sudo is correct here) ──────
info "Updating apt package lists..."
sudo apt-get update -y

info "Installing system dependencies..."
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    python3-setuptools \
    i2c-tools \
    libgpiod-dev \
    python3-libgpiod
success "System packages installed."

# ── 2a. libgpiod2 (needed by adafruit-circuitpython-dht) ─────
# libgpiod2 was superseded by libgpiod3 on Bookworm — try both,
# fail gracefully so set -e does not abort the whole install.
info "Installing libgpiod2 (DHT sensor dependency)..."
if sudo apt-get install -y libgpiod2 2>/dev/null; then
    success "libgpiod2 installed."
else
    warn "libgpiod2 not found in apt repos (expected on Bookworm) — trying libgpiod3..."
    if sudo apt-get install -y libgpiod3 2>/dev/null; then
        success "libgpiod3 installed as substitute."
    else
        warn "Neither libgpiod2 nor libgpiod3 found — DHT sensor may not work."
    fi
fi

# ── 3. Enable hardware interfaces ────────────────────────────
info "Enabling I2C interface..."
sudo raspi-config nonint do_i2c 0

info "Enabling SPI interface..."
sudo raspi-config nonint do_spi 0

info "Enabling Serial hardware..."
sudo raspi-config nonint do_serial_hw 0
success "Hardware interfaces enabled."

# ── 4. Virtual environment setup ─────────────────────────────
if [ ! -d "$VENV_DIR" ]; then
    info "Creating virtual environment at $VENV_DIR ..."
    python3 -m venv "$VENV_DIR" --system-site-packages
    success "Virtual environment created."
else
    warn "Virtual environment already exists at $VENV_DIR — skipping creation."
fi

# ── Use the venv's binaries explicitly from here on ──────────
# This guarantees installs go into venv regardless of whether
# the shell has the venv activated or not.
VENV_PYTHON="$VENV_DIR/bin/python3"
VENV_PIP="$VENV_DIR/bin/pip"

# Quick sanity check — confirm pip resolves inside the venv
info "Confirming pip is inside the venv..."
WHICH_PIP=$("$VENV_PYTHON" -m pip --version | awk '{print $4}')
info "pip location: $WHICH_PIP"
if [[ "$WHICH_PIP" != "$VENV_DIR"* ]]; then
    error "pip is not resolving inside the venv at $VENV_DIR — aborting."
fi
success "pip confirmed inside venv."

# ── 5. Upgrade pip & setuptools ──────────────────────────────
info "Upgrading pip and setuptools..."
"$VENV_PIP" install --upgrade pip setuptools
success "pip and setuptools upgraded."

# ══════════════════════════════════════════════════════════════
#  LIGHT CONTROL SCRIPT DEPENDENCIES
# ══════════════════════════════════════════════════════════════

# ── 6. Adafruit Blinka ────────────────────────────────────────
info "Installing Adafruit-Blinka (provides 'board', 'busio', etc.)..."
"$VENV_PIP" install --upgrade-strategy only-if-needed adafruit-blinka adafruit-platformdetect
success "Adafruit-Blinka installed."

# ── 6a. Configure Blinka for Raspberry Pi ────────────────────
info "Configuring Blinka for Raspberry Pi..."
if "$VENV_PYTHON" -c "import adafruit_platformdetect; d = adafruit_platformdetect.Detector(); print(d.board.id)" 2>/dev/null | grep -q "RASPBERRY"; then
    export BLINKA_RASPBERRY_PI=1
    if ! grep -q "BLINKA_RASPBERRY_PI" "$HOME/.bashrc"; then
        echo "" >> "$HOME/.bashrc"
        echo "# Adafruit Blinka — Raspberry Pi mode" >> "$HOME/.bashrc"
        echo "export BLINKA_RASPBERRY_PI=1" >> "$HOME/.bashrc"
        success "BLINKA_RASPBERRY_PI written to ~/.bashrc"
    else
        warn "BLINKA_RASPBERRY_PI already set in ~/.bashrc — skipping."
    fi
else
    warn "Could not auto-detect Raspberry Pi board — you may need to set manually:"
    warn "  export BLINKA_RASPBERRY_PI=1"
fi
success "Blinka configured."

# ── 7. NeoPixel library ───────────────────────────────────────
info "Installing adafruit-circuitpython-neopixel..."
"$VENV_PIP" install --upgrade-strategy only-if-needed adafruit-circuitpython-neopixel
success "NeoPixel library installed."

# ── 8. TSL2591 sensor library ────────────────────────────────
info "Installing adafruit-circuitpython-tsl2591 (optional sensor)..."
"$VENV_PIP" install --upgrade-strategy only-if-needed adafruit-circuitpython-tsl2591
success "TSL2591 library installed."

# ── 9. NumPy ─────────────────────────────────────────────────
info "Installing numpy..."
"$VENV_PIP" install --upgrade-strategy only-if-needed numpy
success "NumPy installed."

# ══════════════════════════════════════════════════════════════
#  VISUALIZE.PY DEPENDENCIES
# ══════════════════════════════════════════════════════════════

# ── 10. Pandas ───────────────────────────────────────────────
info "Installing pandas..."
"$VENV_PIP" install --upgrade-strategy only-if-needed pandas
success "Pandas installed."

# ── 11. Matplotlib ───────────────────────────────────────────
info "Installing matplotlib..."
"$VENV_PIP" install --upgrade-strategy only-if-needed matplotlib
success "Matplotlib installed."

# ══════════════════════════════════════════════════════════════
#  GPIO / HARDWARE DEPENDENCIES
# ══════════════════════════════════════════════════════════════

# ── 12. RPi.GPIO → rpi-lgpio (Pi 5 compatible drop-in) ───────
# RPi.GPIO does not work on Raspberry Pi 5 (RP1 I/O chip).
# rpi-lgpio provides the exact same API so no code changes needed.
info "Removing RPi.GPIO if present and installing rpi-lgpio..."
"$VENV_PIP" uninstall -y RPi.GPIO 2>/dev/null || true
"$VENV_PIP" install --upgrade-strategy only-if-needed rpi-lgpio
success "rpi-lgpio installed (RPi.GPIO drop-in replacement)."

# ── 13. Adafruit CircuitPython DHT (replaces legacy Adafruit_DHT) ──
# The old Adafruit_DHT library is deprecated and does not install
# cleanly on modern Raspberry Pi OS. Use adafruit-circuitpython-dht.
# Note: your scripts using 'import Adafruit_DHT' will need updating
# to 'import adafruit_dht' with the new API.
info "Installing adafruit-circuitpython-dht (replaces Adafruit_DHT)..."
"$VENV_PIP" install --upgrade-strategy only-if-needed adafruit-circuitpython-dht
success "CircuitPython DHT installed."

# ══════════════════════════════════════════════════════════════
#  COMPUTER VISION DEPENDENCIES
# ══════════════════════════════════════════════════════════════

# ── 14. OpenCV ───────────────────────────────────────────────
info "Installing OpenCV (cv2)..."
"$VENV_PIP" install --upgrade-strategy only-if-needed opencv-python
success "OpenCV installed."

# ══════════════════════════════════════════════════════════════
#  VERIFY ALL IMPORTS
# ══════════════════════════════════════════════════════════════

# ── 15. Verify all imports ────────────────────────────────────
info "Verifying all imports..."
"$VENV_PYTHON" - <<'EOF'
import importlib, sys

required = {
    "board":            "adafruit-blinka",
    "busio":            "adafruit-blinka",
    "neopixel":         "adafruit-circuitpython-neopixel",
    "numpy":            "numpy",
    "pandas":           "pandas",
    "matplotlib":       "matplotlib",
    "matplotlib.dates": "matplotlib",
    "cv2":              "opencv-python",
    "RPi.GPIO":         "rpi-lgpio",
}
optional = {
    "adafruit_tsl2591": "adafruit-circuitpython-tsl2591",
    "adafruit_dht":     "adafruit-circuitpython-dht",
}

all_ok = True
print("\n  ── Required ──────────────────────────────")
for mod, pkg in required.items():
    try:
        importlib.import_module(mod)
        print(f"  ✅  {mod}")
    except ImportError:
        print(f"  ❌  {mod}  (install: pip install {pkg})")
        all_ok = False

print("\n  ── Optional ──────────────────────────────")
for mod, pkg in optional.items():
    try:
        importlib.import_module(mod)
        print(f"  ✅  {mod}  (optional)")
    except ImportError:
        print(f"  ⚠️   {mod}  (optional — sensor features disabled)")

print()
sys.exit(0 if all_ok else 1)
EOF

success "Import verification complete."

# ── 16. Done ─────────────────────────────────────────────────
echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}  ✅  Installation complete!${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo -e "To activate your environment in future sessions, run:"
echo -e "  ${CYAN}source $VENV_DIR/bin/activate${NC}"
echo ""
echo -e "To run the light control script:"
echo -e "  ${CYAN}source $VENV_DIR/bin/activate && python3 main.py${NC}"
echo ""
echo -e "To run the visualizer manually:"
echo -e "  ${CYAN}source $VENV_DIR/bin/activate && python3 visualize.py${NC}"
echo ""
echo -e "${YELLOW}[NOTE]${NC}  Scripts using 'import Adafruit_DHT' must be updated to"
echo -e "        use 'import adafruit_dht' — the old library is deprecated."
echo ""
warn "A reboot is recommended to ensure all hardware interfaces are active."
read -rp "Reboot now? (y/n, default n): " REBOOT
if [[ "$REBOOT" =~ ^[Yy]$ ]]; then
    sudo reboot
fi