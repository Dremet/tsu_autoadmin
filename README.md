# TSU TripleHeat / Auto-Admin

Collection of scripts that allow automatic (no admin needed) scheduling/management of race events on a dedicated server in Turbo Sliders Unlimited.

All .src, .py and .sh files need to be placed in the config/Scripts folder of the dedicated server and automaticScripts need to be enabled.

## Session init/end - Event init/end files

This project provides all four types of automatic scripts along with .sh and .py files to easily and dynamically change what they do.

Keep in mind that one session can consist of multiple events (not the other way around!).

sessioninit:
- that one is empty in this project because some init stuff is done in the auto script run via cronjob, see below, but it is included in case it makes sense to use it in someone else's use case

eventinit:
- randomly sets fuel consumption and tire degradation (within certain limits) so that there is some variety

eventend:
- use result stats file to calculate elo changes

sessionend:
- continues to session init screen (preparation for next day)
- tells people that session has ended
- turns off the timer


## autorun.src

Some things should happen at a certain time of the day and not at session init/end or event init/end, especially if you want to schedule a race at a certain time of the day. 

You can use a cronjob to run the create_autorun.py file at a certain time of the day and provide the function name as an argument like `python3 create_autorun.py announce_1_minute` to send a message to the server that the session will start in 1 minute.
The most important use case though is to actually start the session. That one turns on the time, sends some messages, resets admins, clears levels and sets some randomly chosen levels out of a pool of levels.
