from datetime import datetime
import board
import neopixel
import time
import numpy as np
import pdb
import argparse
import csv
import digitalio
import sys
import os
import re

class Light():
    def __init__(self, pin=board.D18, num_lights=50):
        self.pin = pin
        self.num_lights = num_lights
        self.pixels = neopixel.NeoPixel(self.pin, self.num_lights, auto_write=False)
        self.pixels.fill(0)
        self.max_val = num_lights * 255
        self.curr_val = (0, 0)

    def set_val(self, prop_val=0, abs_val=None):
        update = False
        if abs_val is None:
            abs_val = round(prop_val * self.max_val)
        else:
            assert isinstance(abs_val, int), print("type(abs_val) must be int")
            assert abs_val in range(self.max_val), print("abs_val must be in range(self.max_val)")
            update = True
        base_val = int(abs_val / self.num_lights)
        row_val = int(abs_val % self.num_lights)
        row_change = row_val - self.curr_val[1]
        base_change = base_val - self.curr_val[0]
        change_val = 1
        change_inds = np.random.choice(range(self.num_lights), row_val, replace=False)
        if abs_val != self.abs_val() or update:
            if base_change == 0 and self.curr_val[1] != 0:
                if row_change > 0:
                    free_inds = np.where(np.round(np.mean(self.pixels, 1)).astype(int) - base_val == 0)[0]
                    try:
                        change_inds = np.random.choice(free_inds, row_change, replace=False)
                    except:
                        pdb.set_trace()
                elif row_change < 0:
                    change_val = 0
                    free_inds = np.where(np.round(np.mean(self.pixels, 1)).astype(int) - base_val == 1)[0]
                    change_inds = np.random.choice(free_inds, -row_change, replace=False)
                elif row_change == 0:
                    return
            else:
                self.pixels.fill((base_val, base_val, base_val))
                try:
                    change_inds = np.random.choice(range(self.num_lights), row_val, replace=False)
                except:
                    pdb.set_trace()
            change_val += base_val
            for ind in change_inds:
                self.pixels[ind] = (change_val, change_val, change_val)
            actual = np.array(self.pixels).mean(1).sum()
            if actual > abs_val:
                pdb.set_trace()
            self.curr_val = (base_val, row_val)
            # print(base_val, row_val)
            self.pixels.show()

    def abs_val(self):
        return self.curr_val[0] * 60 + self.curr_val[1]

    def test(self):
        vals = np.sin(np.linspace(0, 5 * np.pi, 1000))
        vals += 1
        vals /= 2
        for val in vals:
            self.set_val(val)
            time.sleep(.01)
        self.set_val()

    def getargs(self):
        parser = argparse.ArgumentParser(usage='%(prog)s [options]', description="Run light control")
        mode = parser.add_mutually_exclusive_group()
        mode.add_argument('--test', default=False, action="store_true", help='Force system time update')
        mode.add_argument('--setup', default=False, action="store_true", help='describe light cycle parameters')
        mode.add_argument('--logger', default=False, action="store_true", help='describe light cycle parameters')
        args = parser.parse_args()
        return args


def read_sensor(sensor):
    try:
        return sensor.lux, sensor.visible, sensor.infrared
    except Exception as e:
        print(f"Sensor read error: {e}")
        return None, None, None


if __name__ == '__main__':
    light1 = Light(pin=board.D10)
    light2 = Light(pin=board.D12)
    light3 = Light(pin=board.D18)
    light4 = Light(pin=board.D21)

    start_sunrise = 7
    start_sunset = 19
    twilight_duration = 1.5
    min_val = 0
    max_val = 0.2

    args = light1.getargs()

    # --- Logging setup ---
    log_input = input("Enable data logging? (y/n, default n): ").strip().lower()
    logging_enabled = log_input == 'y'

    if logging_enabled:
        import adafruit_tsl2591
        i2c = board.I2C()

        gpio17 = digitalio.DigitalInOut(board.D17)
        gpio17.direction = digitalio.Direction.OUTPUT

        gpio17.value = True
        time.sleep(0.1)
        sensor_bottom = adafruit_tsl2591.TSL2591(i2c)

        gpio17.value = False
        time.sleep(0.1)
        sensor_top = adafruit_tsl2591.TSL2591(i2c)

        log_dir = "data"
        os.makedirs(log_dir, exist_ok=True)

        default_name = "sensor_log"
        user_input = input(f"Enter log file name (press enter for default '{default_name}'): ").strip()
        base_name = re.sub(r'[<>:"/\\|?*]', '_', user_input) if user_input else default_name

        log_filename = os.path.join(log_dir, f"{base_name}.csv")
        counter = 1
        while os.path.exists(log_filename):
            log_filename = os.path.join(log_dir, f"{base_name}_{counter}.csv")
            counter += 1

        print(f"Logging to: {log_filename}")
        log_file = open(log_filename, 'w', newline='')
        writer = csv.writer(log_file)
        writer.writerow([
            'timestamp',
            'set_val',
            'top_lux', 'top_visible', 'top_ir',
            'bottom_lux', 'bottom_visible', 'bottom_ir'
        ])

    if args.test:
        light1.test()
        light2.test()
        light3.test()
        light4.test()

    if args.setup:
        print(f"start sunrise: {start_sunrise}")
        print(f"start sunset: {start_sunset}")
        print(f"twilight duration: {twilight_duration}")
        print(f"minimum light value: {min_val}")
        print(f"maximum light value: {max_val}")
        flag = input("Are these values correct (y/n): ")
        if flag == "n":
            sys.exit("Update correct parameters in script")

    try:
        while True:
            now = datetime.now()
            timestamp = now.isoformat()
            now_h = now.hour + now.minute/60 + now.second/3600 + now.microsecond/(3600*1000000)

            if now_h < start_sunrise:
                val = min_val
            elif now_h < start_sunrise + twilight_duration:
                prop = (now_h - start_sunrise) / twilight_duration
                val = prop * max_val
            elif now_h < start_sunset:
                val = max_val
            elif now_h < start_sunset + twilight_duration:
                prop = (now_h - start_sunset) / twilight_duration
                val = (1 - prop) * max_val
            else:
                val = min_val

            light1.set_val(val)
            light2.set_val(val)
            light3.set_val(val)
            light4.set_val(val)

            if logging_enabled:
                gpio17.value = False
                time.sleep(0.005)
                s_top_lux, s_top_vis, s_top_ir = read_sensor(sensor_top)

                gpio17.value = True
                time.sleep(0.005)
                s_bot_lux, s_bot_vis, s_bot_ir = read_sensor(sensor_bottom)

                writer.writerow([timestamp, val, s_top_lux, s_top_vis, s_top_ir, s_bot_lux, s_bot_vis, s_bot_ir])
                log_file.flush()

            time.sleep(.5)

    finally:
        if logging_enabled:
            log_file.close()
        light1.set_val()
        light2.set_val()
        light3.set_val()
        light4.set_val()
