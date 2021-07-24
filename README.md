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

### CLI Commands
`add`: Adds a habit for you to track  
`finish`: Finishes a habit and adds score to your streaks  
`stopwatch`: Start a stopwatch   
`delete`: Delete a habit  
`list`: Lists all your habits, and the stats for each one  
`license`: Shows the license
`system`: System info  
`remind`: Set time for pushover reminder (you need pushover)  

### Webserver
`pip3 install flask`  
Run the webserver/main.py  
The website is found at `127.0.0.1:4321`  

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
