#!/usr/bin/env python3

# To run this you probably need to:
# pip install pyvesync
# pip install python-dotenv

import os
import json

from http.server import BaseHTTPRequestHandler, HTTPServer
from pyvesync import VeSync
from dotenv import load_dotenv
load_dotenv()

# Setup VeSync, login, and get initial device info
vesync = VeSync(os.getenv("VESYNC_USERNAME"), os.getenv("VESYNC_PASSWORD"))
vesync.login()
vesync.update()
humidifier = json.loads(vesync.fans[0].displayJSON())

# Setup server response
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if (self.path == "/metrics"):
            vesync.update()
            humidifier = json.loads(vesync.fans[0].displayJSON())
            cid = humidifier["CID"]
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("# HELP vesync_humidity_ratio The current humidity.\n", "utf-8"))
            self.wfile.write(bytes("# TYPE vesync_humidity_ratio gauge\n", "utf-8"))
            self.wfile.write(bytes(f"vesync_humidity_ratio{{CID=\"{cid}\"}} {int(humidifier['Humidity']) / 100}\n", "utf-8"))
            self.wfile.write(bytes("# HELP vesync_target_humidity_ratio The target humidity.\n", "utf-8"))
            self.wfile.write(bytes("# TYPE vesync_target_humidity_ratio gauge\n", "utf-8"))
            self.wfile.write(bytes(f"vesync_target_humidity_ratio{{CID=\"{cid}\"}} {int(humidifier['Auto Target Humidity']) / 100}\n", "utf-8"))
            self.wfile.write(bytes("# HELP vesync_mist_level The current mist level.\n", "utf-8"))
            self.wfile.write(bytes("# TYPE vesync_mist_level gauge\n", "utf-8"))
            self.wfile.write(bytes(f"vesync_mist_level{{CID=\"{cid}\"}} {humidifier['Mist Level']}\n", "utf-8"))
            self.wfile.write(bytes("# HELP vesync_mist_virtual_level The current mist virtual level.\n", "utf-8"))
            self.wfile.write(bytes("# TYPE vesync_mist_virtual_level gauge\n", "utf-8"))
            self.wfile.write(bytes(f"vesync_mist_virtual_level{{CID=\"{cid}\"}} {humidifier['Mist Virtual Level']}\n", "utf-8"))
            self.wfile.write(bytes("# HELP vesync_night_light_brightness The night light brightness.\n", "utf-8"))
            self.wfile.write(bytes("# TYPE vesync_night_light_brightness gauge\n", "utf-8"))
            self.wfile.write(bytes(f"vesync_night_light_brightness{{CID=\"{cid}\"}} {humidifier['Night Light Brightness']}\n", "utf-8"))
            self.wfile.write(bytes("# HELP vesync_status Device is on.\n", "utf-8"))
            self.wfile.write(bytes("# TYPE vesync_status gauge\n", "utf-8"))
            self.wfile.write(bytes(f"vesync_status{{CID=\"{cid}\"}} {1 if humidifier['Status'] == 'on' else 0}\n", "utf-8"))
            self.wfile.write(bytes("# HELP vesync_online Device is online.\n", "utf-8"))
            self.wfile.write(bytes("# TYPE vesync_online gauge\n", "utf-8"))
            self.wfile.write(bytes(f"vesync_online{{CID=\"{cid}\"}} {1 if humidifier['Online'] == 'online' else 0}\n", "utf-8"))
            self.wfile.write(bytes("# HELP vesync_mode_auto Auto mode enabled.\n", "utf-8"))
            self.wfile.write(bytes("# TYPE vesync_mode_auto gauge\n", "utf-8"))
            self.wfile.write(bytes(f"vesync_mode_auto{{CID=\"{cid}\"}} {1 if humidifier['Mode'] == 'auto' else 0}\n", "utf-8"))
            self.wfile.write(bytes("# HELP vesync_water_lacks Water level low.\n", "utf-8"))
            self.wfile.write(bytes("# TYPE vesync_water_lacks gauge\n", "utf-8"))
            self.wfile.write(bytes(f"vesync_water_lacks{{CID=\"{cid}\"}} {1 if humidifier['Water Lacks'] == True else 0}\n", "utf-8"))
            self.wfile.write(bytes("# HELP vesync_humidity_high Humidity too high.\n", "utf-8"))
            self.wfile.write(bytes("# TYPE vesync_humidity_high gauge\n", "utf-8"))
            self.wfile.write(bytes(f"vesync_humidity_high{{CID=\"{cid}\"}} {1 if humidifier['Humidity High'] == True else 0}\n", "utf-8"))
            self.wfile.write(bytes("# HELP vesync_water_tank_lifted Water tank missing.\n", "utf-8"))
            self.wfile.write(bytes("# TYPE vesync_water_tank_lifted gauge\n", "utf-8"))
            self.wfile.write(bytes(f"vesync_water_tank_lifted{{CID=\"{cid}\"}} {1 if humidifier['Water Tank Lifted'] == True else 0}\n", "utf-8"))
            self.wfile.write(bytes("# HELP vesync_display_enabled Display is enabled.\n", "utf-8"))
            self.wfile.write(bytes("# TYPE vesync_display_enabled gauge\n", "utf-8"))
            self.wfile.write(bytes(f"vesync_display_enabled{{CID=\"{cid}\"}} {1 if humidifier['Display'] == True else 0}\n", "utf-8"))
            self.wfile.write(bytes("# HELP vesync_automatic_stop_reach_target Automatic stop reach target?\n", "utf-8"))
            self.wfile.write(bytes("# TYPE vesync_automatic_stop_reach_target gauge\n", "utf-8"))
            self.wfile.write(bytes(f"vesync_automatic_stop_reach_target{{CID=\"{cid}\"}} {1 if humidifier['Automatic Stop Reach Target'] == True else 0}\n", "utf-8"))
            self.wfile.write(bytes("# HELP vesync_automatic_stop Automatic stop?\n", "utf-8"))
            self.wfile.write(bytes("# TYPE vesync_automatic_stop gauge\n", "utf-8"))
            self.wfile.write(bytes(f"vesync_automatic_stop{{CID=\"{cid}\"}} {1 if humidifier['Automatic Stop'] == True else 0}\n", "utf-8"))
        else:
            self.send_response(501)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("501 Not Implemented", "utf-8"))

# Start server
server = HTTPServer((os.getenv("HOSTNAME"), int(os.getenv("PORT"))), MyServer)
print("Server started http://%s:%s" % (os.getenv("HOSTNAME"), os.getenv("PORT")))

try:
    server.serve_forever()
except KeyboardInterrupt:
    pass

server.server_close()
print("Server stopped.")