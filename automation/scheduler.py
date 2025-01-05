import schedule
import time
from task_manager import TaskManager

class Scheduler:
    def __init__(self):
        self.task_manager = TaskManager()

    def schedule_task(self, task_name, interval, action):
        if interval == 'daily':
            schedule.every().day.at(action).do(self.task_manager.run_task, task_name)
        elif interval == 'hourly':
            schedule.every().hour.do(self.task_manager.run_task, task_name)
        print(f"Task {task_name} scheduled at {interval}.")

    def run(self):
        while True:
            schedule.run_pending()
            time.sleep(1)
