import time
from blink1.blink1 import blink1, Blink1

# Print Blink Serial Information
blink1_serials = Blink1.list()
print("blink(1) devices found: " + ','.join(blink1_serials))

# Loop through shit
while True:
  with blink1() as b1:
    b1.fade_to_color(1500, 'red')
    b1.fade_to_color(1500, 'green')
    b1.fade_to_color(1500, 'blue')
    b1.fade_to_color(1500, 'white')
    time.sleep(5)