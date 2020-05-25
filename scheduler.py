import threading
import time
from typing import Dict, Tuple, Callable, NoReturn, Any, Optional
from random import choice

func_type = Callable[[], Any]
schedule: Dict[str, Tuple[float, func_type]] = {}
schedule_lock = threading.RLock()
digits: str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
paused_tasks = {}


def scheduler() -> NoReturn:
	while True:
		if len(schedule) > 1:
			print(schedule)
		time.sleep(1)
		t1: float = time.time()
		with schedule_lock:
			for id, task in [*schedule.items()]:
				if task[0] <= t1:
					task[1]()
					remove_task(id)


def new_task(t: float, task: func_type) -> str:
	print('adding a new task')
	task_id = ''.join(choice(digits) for i in range(24))
	with schedule_lock:
		schedule[task_id] = (t, task)
	print(schedule[task_id])
	return task_id


def remove_task(id):
	print('removing a task')
	with schedule_lock:
		if id in schedule:
			schedule.pop(id)


def reschedule_task(id: str, time: float) -> bool:
	print('rescheduling a task')
	if id in schedule:
		with schedule_lock:
			schedule[id] = (time, schedule[id][1])
		return True
	else:
		return False


def pause_task(id: Optional[str]) -> None:
	if id not in paused_tasks:
		with schedule_lock:
			paused_tasks[id] = (time.time(), schedule.pop(id))
			print('Pause task...')
	else:
		with schedule_lock:
			time_paused, original_task = paused_tasks[id]
			schedule[id] = (original_task[0] + time.time() - time_paused, original_task[1])
			print('Resume task...')



# Written by Satan0 (twitch.tv)
# Example of use:

# import scheduler
# def do_a_thing()
# 	# now_time = time.time()
# 	# _id = scheduler.new_task(time.time() + duration, func_to_do)
# 	....
#
# def Main():
#     sched = threading.Thread(target=scheduler.scheduler, args=())
#     sched.start()
# 	....
