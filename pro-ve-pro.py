#!/usr/bin/env python3

import os

from pyvesync import VeSync
from dotenv import load_dotenv
load_dotenv()

manager = VeSync(os.getenv("VESYNC_USERNAME"), os.getenv("VESYNC_PASSWORD"))
manager.login()

manager.update()
manager.get_devices()

print(manager.fans[0].displayJSON())