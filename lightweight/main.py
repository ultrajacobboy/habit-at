from light_habit import Habit

client = Habit()
client.welcome()
while True:
    client.is_it_ended()
    client.user_input()