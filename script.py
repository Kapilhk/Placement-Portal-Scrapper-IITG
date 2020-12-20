import subprocess
import time
import os
import random
while True:
    try:
        os.system("scrapper.py")
        tosleep=random.randrange(200, 600)
        #if tosleep>27:
            #tosleep=random.randrange(60, 100)
            #if tosleep>270:
            #    tosleep=random.randrange(300, 480)
        print("wait"+str(tosleep))
        time.sleep(tosleep)
    except KeyboardInterrupt:
        break