from habit import Habit
import time
import multiprocessing

cpu_count = multiprocessing.cpu_count()
if cpu_count < 2:
    print("Sorry. This cannot run with less than 2 cores.")
    sys.exit()
else:
    client = Habit()
    while True:
        try:
            client.welcome()
            client.is_it_ended()
            client.user_input()
        except KeyboardInterrupt:
            print("Type exit or quit!")
        except Exception as e:
            print(f"Something went wrong!\n{e}")
            time.sleep(324)