from ui.runnables import Menu, MsgViewer
from server.interface import SERVER_CONFIG
import subprocess

class MenuTree:
    """
    class to hold all runnables for the menu
    """
    def __init__(self, control):
        self.main = MainMenu([], control)
        self.log = LogMenu([None, None, None, self.main], control)
        self.status = StatusMsg(self.main, control)
        self.main.runnables = [self.status, self.log]
        
        # run main menu
        self.main.run()


class MainMenu(Menu):
    """
    class to build the main menu
    """
    def __init__(self, runnables, *args, **kwargs):
        # Do NOT forget to hand over control
        entries = ["STATUS", "VIEW LOGS", "CURRENT STATS", "WiFi-SETUP", "HALLO"]
        super().__init__(entries, runnables, *args, **kwargs)
        
        
class LogMenu(Menu):
    """
    class to build the log menu
    """
    def __init__(self, runnables, *args, **kwargs):
        # Do NOT forget to hand over control
        entries = ["Data Measurements", "Errors", "Info", "BACK"]
        super().__init__(entries, runnables, *args, **kwargs)


def cmd_output(command):
    # calls the command and returns its output as String
    p = subprocess.run(command, shell=True, capture_output=True, text=True)
    return p.stdout


class StatusMsg(MsgViewer):
    """
    class to build a message view with core status variables
    """
    def __init__(self, *args, **kwargs):
        # Hand over no mesage for now
        super().__init__('', *args, **kwargs)
        
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
                # test ping to psuserver
                msg += "Current PING to server:\n"
                ping = cmd_output("ping -c 1 " + SERVER_CONFIG['URL'].split('//')[1] + " | grep avg").split('/')
                
                if len(ping) == 7:
                    msg += '{} {}'.format(ping[4], ping[6].split(' ')[1])
                else:
                    msg += "No Server Connection\n"
            else:
                msg += "No Network Connection\n"
        except Exception as e:
            print(e)
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
        except Exception as e:
            print(e)
            msg += "Could not gather information\n"

        self.message = msg
        self.top = 0
        self.split_into_lines()
        super().run()
        
