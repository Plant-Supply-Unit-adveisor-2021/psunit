from ui.runnables import Menu, DynamicMsgViewer, LogFileViewer, ConfirmationViewer
from server.interface import get_server_config, register_at_server
from sensors.filllevel import set_extreme_value
from settings import DATA_DIR
import subprocess
from os.path import join
from traceback import format_exc
from threading import Thread
from time import sleep

class MenuTree:
    """
    class to hold all runnables for the menu
    """
    def __init__(self, control):
        self.main = MainMenu([], control)
        self.status = StatusMsg(self.main, control)
        self.log = LogMenu(self.main, control)
        self.sensors = SensorsMenu(self.main, control)
        self.registration = RegistrationMenu(self.main, control)
        self.wifi = WiFiMenu(self.main, control)
        self.main.runnables = [self.status, self.log, self.sensors, self.registration, self.wifi]
        
        # run main menu
        self.main.run()


class MainMenu(Menu):
    """
    class to build the main menu
    """
    def __init__(self, runnables, *args, **kwargs):
        # Do NOT forget to hand over control
        entries = ["STATUS", "VIEW LOGS", "SENSORS", "REGISTRATION", "WiFi-SETUP"]
        super().__init__(entries, runnables, *args, **kwargs)
        
        
class LogMenu(Menu):
    """
    class to build the log menu
    """
    def __init__(self, back_view, *args, **kwargs):
        # Do NOT forget to hand over control
        entries = ["measure.log", "watering.log", "push.log", "BACK"]
        runnables = []
        runnables.append(LogFileViewer(join(DATA_DIR, 'measure.log'), self,*args, **kwargs))
        runnables.append(LogFileViewer(join(DATA_DIR, 'watering.log'), self, *args, **kwargs))
        runnables.append(LogFileViewer(join(DATA_DIR, 'push.log'), self, *args, **kwargs))
        runnables.append(back_view)
        super().__init__(entries, runnables, *args, **kwargs)


def cmd_output(command):
    # calls the command and returns its output as String
    p = subprocess.run(command, shell=True, capture_output=True, text=True)
    return p.stdout


class StatusMsg(DynamicMsgViewer):
    """
    class to build a message view with core status variables
    """
    def run(self):
        """
        called to show the stats
        """
        msg = "Current IP-Address:\n"
        try:
            ip = cmd_output("hostname -I").split(" ")[0]
            if len(ip) >= 7:
                # network connection up
                msg += ip + "\n"
                url = get_server_config()['URL']
                # test ping to psuserver
                msg += "Current PING to server:\n"
                ping = cmd_output("ping -c 1 " + url.split('//')[1] + " | grep avg").split('/')
                
                if len(ping) == 7:
                    msg += '{} {}'.format(ping[4], ping[6].split(' ')[1])
                else:
                    msg += "No Server Connection\n"
            else:
                msg += "No Network Connection\n"
        except Exception:
            print(format_exc())
            msg += "Could not gather information\n"
            
        msg += "Current SD-Card Usage:\n"
        try:
            # get the current storage level
            storage = cmd_output("df -h | grep /dev/root").split(' ')
            i = 1
            x = 1
            while storage[1] == "" or storage[2]== "":
                if storage[x] == '':
                    storage[x] = storage[i+1]
                    i += 1
                else:
                    x += 1
                    i += 1
            msg += '{1} of {0}\n'.format(storage[1], storage[2])
        except Exception:
            print(format_exc())
            msg += "Could not gather information\n"

        self.message = msg + "To refresh just go back and reenter this view."
        super().run()


class PairingKeyViewer(DynamicMsgViewer):
        # viewer to show the current pairing key
        def run(self):
            try:
                key = get_server_config()['pairing_key']
                self.message = "Pairing Key of this PSU:\n"
                self.message += key + '\n'
                self.message += "Note: The key is a hexadecimal number."
            except Exception:
                # print(format_exc())
                self.message = "Currently there is no pairing key for this "
                self.message += "PSU available. Please register this PSU first."

            super().run()
            
            
class RSAKeyViewer(DynamicMsgViewer):
        # viewer to show the current rsa key pair
        def run(self):
            try:
                key = get_server_config()['public_key']
                self.message = "Public Key of this PSU:\n"
                self.message += key + '\n'
                key = get_server_config()['private_key']
                self.message += "Private Key of this PSU:\n"
                self.message += key + '\n'
                self.message += "Note: These keys are RSA-2048 keys."
            except Exception:
                # print(format_exc())
                self.message = "Currently there is no key pair for this "
                self.message += "PSU available. Please register this PSU first."

            super().run()
            
            
class IdentityKeyViewer(DynamicMsgViewer):
        # viewer to show the identity
        def run(self):
            try:
                key = get_server_config()['identity_key']
                self.message = "Identity Key of this PSU:\n"
                self.message += key + '\n'
                self.message += "Note: This key is randomly generated by the server."
            except Exception:
                # print(format_exc())
                self.message = "Currently there is no identity key this "
                self.message += "PSU available. Please register this PSU first."

            super().run()
            
            
class RegistrationViewer(DynamicMsgViewer):
    # viewer to register PSU at the server and show the success of this operation
    def run(self):
        self.timeout = False # NO TIMEOUT
        self.message = "Trying to register PSU at server. This might take a short while. Keep this view open!"
        super().run()
        try:
            if register_at_server():
                self.message += "\nSuccessfully registerd PSU. Please go to psu-server.duckdns.org and claim this PSU via registering it."
            else:
                self.message += "\nSorry. This was not successful. Please try later or contact support."
            super().run()
        except Exception:
            print(format_exc)
            self.message += "\nSorry. This was not successful. Please try later or contact support."
            super().run()


class RegistrationMenu(Menu):
    """
    menu holding all the stuff which is necessary for the registration
    """
    
    def __init__(self, back_view, *args, **kwargs):
        entries = []
        runnables = []
        entries.append("Current Pairing Key")
        runnables.append(PairingKeyViewer(self, *args, **kwargs))
        entries.append("Register PSU")
        confirm_msg = "Going on will reset this PSUs config on the server completly. Additonally old measurements won't be linked to ths new PSU instance."
        rg_view = RegistrationViewer(self, *args, **kwargs)
        runnables.append(ConfirmationViewer(confirm_msg, rg_view, self, *args, **kwargs))
        entries.append("RSA Key Pair")
        runnables.append(RSAKeyViewer(self, *args, **kwargs))
        entries.append("Identity Key")
        runnables.append(IdentityKeyViewer(self, *args, **kwargs))
        entries.append("BACK")
        runnables.append(back_view)
        super().__init__(entries, runnables, *args, **kwargs)
        

def get_wifi_status():
    # returns dict with values from wpa_cli -i wlan0 status
    data = cmd_output("wpa_cli -i wlan0 status").split('\n')
    info = dict()
    for d in data:
        vs = d.split('=')
        if len(vs) == 2:
            info[vs[0]] = vs[1]
    return info


class WiFiStatus(DynamicMsgViewer):
    """
    view to show the current WiFi-staus
    """
    def run(self):
        msg = "Current WiFi status:\n\n"
        
        try:
            # gather wifi status and put infos in a dict
            info = get_wifi_status()
            if info['wpa_state'] == 'COMPLETED':
                # WiFi connection up
                msg += "Connetion Status:\nWiFi connected\n"
                msg += "SSID: " + info['ssid'] + '\n'
                msg += "IP: " + info['ip_address'] + '\n\n'
            elif info['wpa_state'] == 'INACTIVE' or info['wpa_state'] == 'SCANNING':
                # WiFi connection down
                msg += "Connetion Status:\nWiFi currently not connected. Please consider using WPS Connect to start the WiFi connection.\n\n"
            else:
                # Something weird
                msg += "Looks like your PSU's WiFi-Setup is not in good shape right now, it might even be disabled.\n\n"
            
                
        except Exception:
            print(format_exc())
            msg += "Could not gather information\n"

        self.message = msg + "To refresh just go back and reenter this view."
        super().run()


class WiFiList(DynamicMsgViewer):
    """
    view to show a list of al currently available WiFi-Networks
    """
    def run(self):
        msg = "List of all current available networks:\n\n"
        try:
            # start_scan
            if not cmd_output("wpa_cli -i wlan0 scan") == "OK\n":
                msg += "Sorry. The WiFi-Scan failed\n"
            # get results
            raw = cmd_output("wpa_cli -i wlan0 scan_results")
            for l in raw.split('\n'):
                info = l.split("\t")
                if len(info) != 5:
                    continue
                msg += info[4]
                if 'WPS' in info[3]:
                    msg += " [WPS]"
                msg += '\n'
        except Exception:
            print(format_exc())
            msg += "Could not gather information\n"

        self.message = msg + "\nTo refresh just go back and reenter this view."
        super().run()


class WiFiStatusMonitor(Thread):
    # thread to check the status of WiFi and redirect to WiFiStatus if connected
    
    def __init__(self, view):
        super().__init__(daemon=True)
        self.view = view
        self.stopped = False
    
    def stop(self):
        self.stopped = True
    
    def run(self):
        while True:
            try:
                if self.stopped:
                    break
                if get_wifi_status()['wpa_state'] == 'COMPLETED':
                    # sleep shortly to allow the PSU to get an IP Address
                    sleep(5)
                    self.view.run()
                    break
                sleep(2)
            except:
                print(format_exc())
                break


class WPSConnectViewer(DynamicMsgViewer):
    # viewer to connect PSU to WiFi via WPS
    
    def __init__(self, status_view, *args, **kwargs):
        # Do NOT forget to hand over back_view and control
        self.status_view = status_view
        super().__init__(*args, **kwargs)
    
    def run(self):
        self.timeout = False # NO TIMEOUT
        self.message = "WPS-Connect\n"
        try:
            if cmd_output("wpa_cli -i wlan0 wps_pbc") != "OK\n":
                self.message += "Sorry. There went something wrong during preparing this PSU for WPS Connect.\n"
            else:
                self.message += "Your PSU is now in WPS-Connect-Mode for the next 2 minutes.\n"
                self.message += "For connecting just press the WPS Connect Button of your WiFi router.\n"
                self.message += "You might need to activate WPS Push-Button-Configuration in your routers settings.\n"
                self.message += "After the PSU has been conntected to your WiFi you will be presented with the current WiFi status.\n"
                self.message += "Closing this view will cancel WPS-Connect-Mode.\n"
                self.monitor = WiFiStatusMonitor(self.status_view)
                self.monitor.start()
        except Exception:
            print(format_exc)
            self.message += "Sorry. There was an error during preparing this PSU for WPS Connect."
        super().run()
        
    def rot_push(self):
        # cancel wps mode
        cmd_output("wpa_cli -i wlan0 wps_cancel")
        # cancel monitor
        if self.monitor:
            self.monitor.stop()
        super().rot_push()


class WiFiMenu(Menu):
    """
    menu holding all the stuff which is necessary for the WiFi-Setup
    """
    
    def __init__(self, back_view, *args, **kwargs):
        entries = []
        runnables = []
        entries.append("WiFi Status")
        status = WiFiStatus(self, *args, **kwargs)
        runnables.append(status)
        entries.append("WPS Connect")
        runnables.append(WPSConnectViewer(status, self, *args, **kwargs))
        entries.append("WiFi Networks")
        runnables.append(WiFiList(self, *args, **kwargs))
        entries.append("BACK")
        runnables.append(back_view)
        super().__init__(entries, runnables, *args, **kwargs)
        

def add_senswarn(view, back_view, *args, **kwargs):
    # function to add the sensors warning to views
    warn = "Attention:\n This action may interfere with the automatic measurements "
    warn += "of your PSU. Pleae do NOT run at minute 0, 15, 30, 45 + 2min of every hour."
    return ConfirmationViewer(warn, view, back_view, *args, **kwargs)


class FilllevelAdjust(DynamicMsgViewer):
    # view to set a new extreme value for the filllevel
    def __init__(self, full, *args, **kwargs):
        # Do NOT forget to hand over back_view and control
        self.full = full # True -> MaxValue: False -> MinValue
        self.ready = False
        super().__init__(*args, **kwargs)
        
    def run(self):
        self.timeout = False # NO TIMEOUT
        self.message = "Taking a lot of measurements to keep the failure rate low ...\n\n"
        self.message += "This might take a while, please wait.\n"
        super().run()
        
        # run set_extreme_value and evaluate success
        if set_extreme_value(self.full):
            self.message = "Taking a lot of measurements to keep the failure rate low ...\n"
            self.message += "Success! New value set. You can now quit."
        else:
            self.message = "Taking a lot of measurements to keep the failure rate low ...\n"
            self.message += "Sorry. Something went wrong please retry later or contact support."
        self.ready = True
        self.timeout = True # Enable timeout
        super().run()
        
    def rot_push(self):
        # only allow quitting if ready
        if self.ready:
            super().rot_push()

class FilllevelMenu(Menu):
    """
    menu holding everzthing considering sensors
    """
    def  __init__(self, back_view, *args, **kwargs):
        entries = []
        runnables = []
        entries.append("Adjust MAX")
        runnables.append(add_senswarn(FilllevelAdjust(True, self, *args, **kwargs), self, *args, **kwargs))
        entries.append("Adjust MIN")
        runnables.append(add_senswarn(FilllevelAdjust(False, self, *args, **kwargs), self, *args, **kwargs))
        entries.append("BACK")
        runnables.append(back_view)
        super().__init__(entries, runnables, *args, **kwargs)

        
class SensorsMenu(Menu):
    """
    menu holding everzthing considering sensors
    """
    def  __init__(self, back_view, *args, **kwargs):
        entries = []
        runnables = []
        entries.append("Filllevel")
        runnables.append(FilllevelMenu(self, *args, **kwargs))
        entries.append("BACK")
        runnables.append(back_view)
        super().__init__(entries, runnables, *args, **kwargs)
