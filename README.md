# Nikke-OL-Summarizer
Summarizes your [Overloaded equipment](https://nikke.gg/overload-equipment/) stats.


## Setup on Windows
1. Install Python
1. Install the requirements, it is recommended to create a virtual environment first:
	- with terminal open in the root of the directory
		```
		python -m venv .\venv
		.\venv\Scripts\activate.bat
		python -m pip install -r requirements.txt
		```

## Running
1. In command line run readmystats.py. Wait until the secondary python window appears and prints "Ready!" Go to NIKKE on desktop and go to a NIKKE in your roster.

	`python readmystats.py`


### Manually Opening Stats
1. Open an equipment and hit `\`. Do this for every equipment.


### Automatically Record Stats
1. Open a NIKKE page and hit `+`. This currently only works for 1080p.
1. When you are done, type `~`.
1. In your command line window, type `~` again to finalize the stats.
1. They should now be printed out like this:
```
TOTAL STATS:
Increase Element Damage Dealt: 23.56
Increase Hit Rate: 13.93
Increase Max Ammunition Capacity: 121.43
Increase ATK: 34.03
Increase Charge Speed: 7.789999999999999
Increase Critical Rate: 5.37
Increase DEF: 4.77
```


## TODO
- Automate the gear selection/screenshotting process
- Allow you to evaluate gear from multiple NIKKE
- Individually store gear stats
- Allow you to store data in a discord bot
- Allow it to run on CUDA. - but I'm lazy and its very small work so I haven't felt the need to do anything


## Limitations
- OCR will sometimes just confused numbers for letters. - I don't think I can catch all of these but I do print these out for the user to use to fill in later.
- Fullscreen only. - because trying to evaluate where everything on the screen is is much more annoying.
- Can't test on 4k. - but I don't think should be an issue.
- Requires Admin in order to run. - because NIKKE eats the inputs otherwise.
- Some numbers are weird (e.g: 7.789999999999999). - because of floats. I honestly can probably fix this later by converting to ints and manually inserting decimals but this is astronomically low priority atm.