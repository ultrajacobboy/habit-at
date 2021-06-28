# Habit-at

Habit-at is a small app that can help track your habits by making streaks  
Habit-at also is 100% open source (duh) and requires no internet connection or external modules for the CLI version (the webserver does require flask `pip3 install flask`)!


## Installation

Use git to clone this repo

```bash
git clone https://github.com/ultrajacobboy/habit-at/tree/main
```

## Usage

### CLI

#### There are two CLI versions; regular and lightweight/main.py  
To the user, they are the same but what are the differences?  
Running regular, habit-at will run a "time check" to check if the day is changed every 25 seconds with the help of threading  
Running lightweight, habit-at will run a "time check" alongside any other command being run.  

#### So who should use lightweight?  
Anyone with less than 2 cores or if you prefer less read and write to files. To check your amount of cores, run corecheck.py  

### CLI Commands
`add`: Adds a habit for you to track  
`finish`: Finishes a habit and adds score to your streaks  
`stopwatch`: Start a stopwatch   
`delete`: Delete a habit  
`list`: Lists all your habits, and the stats for each one  
`license`: Shows the license (Regular only)  
`system`: System info

### Webserver
`pip3 install flask`  
Run the webserver/main.py  
The website is found at `127.0.0.1:4321`  

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
