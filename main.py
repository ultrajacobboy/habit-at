from habit import Habit, bcolors
import multiprocessing

cpu_count = multiprocessing.cpu_count()
if cpu_count < 2:
    print("Sorry. This cannot run with less than 2 cores.")
    sys.exit()
else:
    client = Habit()
    colors = bcolors()
    client.welcome()
    while True:
        try:
            client.is_it_ended()
            client.user_input()
        except KeyboardInterrupt:
            print(f"To quit the program, type {colors.FAIL}exit{colors.ENDC} or {colors.FAIL}quit!{colors.ENDC}")
        except Exception as e:
            print(f"{colors.FAIL}Something went wrong!{colors.ENDC}\n{e}")