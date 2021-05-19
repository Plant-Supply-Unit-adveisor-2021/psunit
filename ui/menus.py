from ui.runnables import Menu, DynamicMsgViewer, LogFileViewer, ConfirmationViewer
from server.interface import get_server_config, register_at_server
from settings import DATA_DIR
import subprocess
from os.path import join
from traceback import format_exc

class MenuTree:
    """
    class to hold all runnables for the menu
    """
    def __init__(self, control):
        self.main = MainMenu([], control)
        self.status = StatusMsg(self.main, control)
        self.log = LogMenu(self.main, control)
        self.registration = RegistrationMenu(self.main, control)
        self.main.runnables = [self.status, self.log, self.registration]
        
        # run main menu
        self.main.run()


class MainMenu(Menu):
    """
    class to build the main menu
    """
    def __init__(self, runnables, *args, **kwargs):
        # Do NOT forget to hand over control
        entries = ["STATUS", "VIEW LOGS", "REGISTRATION", "WiFi-SETUP"]
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

        self.message = msg
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
        
