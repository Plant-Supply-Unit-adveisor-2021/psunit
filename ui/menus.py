from ui.runnables import Menu

class MenuTree:
    """
    class to hold all runnables for the menu
    """
    def __init__(self, control):
        self.main = MainMenu([], control)
        self.log = LogMenu([None, None, None, self.main], control)
        self.main.runnables = [None, self.log]
        
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

