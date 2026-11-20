import sys
from pathlib import Path
import types

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / 'light-emulation' / 'scripts'),
)

if 'board' not in sys.modules:
    board = types.ModuleType('board')
    board.D18 = 18
    sys.modules['board'] = board

if 'neopixel' not in sys.modules:
    sys.modules['neopixel'] = types.ModuleType('neopixel')

from core import light


class FakeLgpio:
    def __init__(self):
        self.calls = []
        self.closed = False

    def gpiochip_open(self, chip):
        self.calls.append(('open', chip))
        return 123

    def gpio_claim_output(self, chip, gpio):
        self.calls.append(('claim', chip, gpio))

    def tx_pwm(self, chip, gpio, frequency, duty):
        self.calls.append(('pwm', chip, gpio, frequency, duty))

    def gpio_write(self, chip, gpio, value):
        self.calls.append(('write', chip, gpio, value))

    def gpiochip_close(self, chip):
        self.calls.append(('close', chip))
        self.closed = True


def test_external_pwm_maps_diel_value_and_turns_off(monkeypatch):
    fake_lgpio = FakeLgpio()
    monkeypatch.setattr(light, 'lgpio', fake_lgpio)

    pwm = light.ExternalPwmLight(
        gpio=18,
        chip=15,
        frequency=1000,
        max_duty=80,
    )
    pwm.set_val(0.25)
    pwm.off()

    assert ('pwm', 123, 18, 1000, 20.0) in fake_lgpio.calls
    assert ('write', 123, 18, 0) in fake_lgpio.calls
    assert ('close', 123) in fake_lgpio.calls


def test_external_pwm_maps_separate_diel_range(monkeypatch):
    fake_lgpio = FakeLgpio()
    monkeypatch.setattr(light, 'lgpio', fake_lgpio)

    pwm = light.ExternalPwmLight(
        gpio=18,
        chip=15,
        frequency=1000,
        min_duty=10,
        max_duty=80,
    )
    pwm.set_val(0.1, 0.0, 0.2)

    assert ('pwm', 123, 18, 1000, 45.0) in fake_lgpio.calls
