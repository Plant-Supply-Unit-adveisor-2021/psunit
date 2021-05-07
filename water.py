from datetime import datetime

from server.interface import get_watering_task, mark_watering_task_executed
from sensors.pump import pump_water

"""
python script called via cron in order to get a watering task and execute ist
"""

print(datetime.now().strftime("Starting water.py at %d.%m.%Y %H:%M:%S"))

id, amount = get_watering_task()
if id >= 0:
    # vaild task
    pump_water(amount)
    print('Watering plant according to task {} with {}ml.'.format(id, amount))
    mark_watering_task_executed(id)
else:
    print("No valid watering task available.")
