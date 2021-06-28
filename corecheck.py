import multiprocessing

cpu_count = multiprocessing.cpu_count()

print(f"You have {cpu_count} cores.")