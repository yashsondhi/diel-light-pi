from datetime import datetime
import board
import neopixel
import time
import numpy as np
import pdb
import argparse

class Light():
    def __init__(self, pin=board.D18, num_lights=60):
        self.pin = pin
        self.num_lights = num_lights
        self.pixels = neopixel.NeoPixel(self.pin, self.num_lights, auto_write=False)
        self.pixels.fill(0)
        self.max_val = num_lights * 255
        self.curr_val = (0, 0)
    def set_val(self, prop_val=0, abs_val=None):
        if abs_val is None:
            abs_val = round(prop_val * self.max_val)
        else:
            assert isinstance(abs_val, int), print("type(abs_val) must be int")
            assert abs_val in range(self.max_val), print("abs_val must be in range(self.max_val)")
        base_val = int(abs_val / self.num_lights)
        row_val = int(abs_val % self.num_lights)
        row_change = row_val - self.curr_val[1]
        base_change = base_val - self.curr_val[0]
        change_val = 1
        change_inds = np.random.choice(range(self.num_lights), row_val, replace=False)
        if abs_val != self.abs_val():
            if base_change == 0 and self.curr_val[1] != 0:
                if row_change > 0:
                    free_inds = np.where(np.mean(self.pixels, 1) - base_val == 0)[0]
                    try:
                        change_inds = np.random.choice(free_inds, row_change, replace=False)
                    except:
                        pdb.set_trace()
                elif row_change < 0:
                    change_val = 0
                    free_inds = np.where(np.mean(self.pixels, 1) - base_val == 1)[0]
                    change_inds = np.random.choice(free_inds, -row_change, replace=False)
            else:
                self.pixels.fill((base_val, base_val, base_val))
                try:
                    change_inds = np.random.choice(range(self.num_lights), row_val, replace=False)
                except:
                    pdb.set_trace()
            change_val += base_val       
            for ind in change_inds:
                self.pixels[ind] = (change_val, change_val, change_val)
            if np.array(self.pixels).mean(1).sum() > abs_val:
                pdb.set_trace()
            self.curr_val = (base_val, row_val)
            print(base_val, row_val)
            self.pixels.show()
    def abs_val(self):
        return self.curr_val[0]*60 + self.curr_val[1]
    def test(self):
        vals = np.sin(np.linspace(0, 5*np.pi, 1000))
        vals += 1
        vals /= 2
        vals /= 1
        for val in vals:
            light.set_val(val)
            time.sleep(.01)
        light.set_val()
    def getargs(self):
        parser = argparse.ArgumentParser(usage='%(prog)s [options]', description="Run light control")
        mode = parser.add_mutually_exclusive_group()
        mode.add_argument('--test', default=False, action="store_true", help='Force system time update')
        mode.add_argument('--setup', default=False, action="store_true",help='describe light cycle parameters project update')
        args = parser.parse_args()
        return (args)
    

if __name__ == '__main__':
    light = Light()
    start_sunrise = 6
    start_sunset = 18
    twilight_duration = 2
    min_val = 0
    max_val = 0.2
    args=light.getargs()
    if(args.test==True):
         light.test()
    if(args.setup==True):
        print(f"start sunrise:{start_sunrise}")
        print(f"start sunset:{start_sunset}")
        print(f"twilight duration:{twilight_duration}")
        print(f"mininmum light value:{min_val}")
        print(f"maximum light value:{max_val}")
        flag=input("Are these values correct (y/n): ")
        if(flag=="n"):
            sys.exit("Update correct parameters in script")            
        
    #To test uncomment and run light.test() in pdb mode
##    setup brightness as a function of time given the above values
    while True:
        now = datetime.now()
        now = now.hour + now.minute/60 + now.second/3600 + now.microsecond/(3600*1000000)
        if now < start_sunrise:
            val = min_val
        elif now < start_sunrise + twilight_duration:
            prop = (now - start_sunrise)/twilight_duration
            val = prop * max_val
        elif now < start_sunset:
            val = max_val
        elif now < start_sunset + twilight_duration:
            prop = (now - start_sunset)/twilight_duration
            val = (1 - prop) * max_val
        else:
            val = min_val
        #pdb.set_trace()
        light.set_val(val)
        time.sleep(.5)
    light.set_val()
