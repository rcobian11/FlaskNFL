# NFL Picks
Web app which gets picks from user and stores selection in a csv file. Python Flask backend html/js front end(Looking to incorporate angularJS).

## Usage
### AWS ElasticBeanstalk (Production)
If deployed to AWS Elastic Beanstalk Production version will be ran and picks.csv will be stored in aws S3 bucket.

### Local (Development)
```bash
pip install -r requirments.txt
```
If ran locally (using `flask run` or `python application.py`) development version will be ran and picks.csv will be stored locally in same directory.

### On first deployment and each new week the config file will need to be created/updated.

## Directories
### /
This is the home directory where users will go to make thier picks. picks will appear in a table with each row containing the favorite team, the spread, and the underdog team. If all fields are not filled out an alert will appear letting the user know that all fields must be correctly filled out. (Example image below *picks.html*)

### /gen_config
The web-app is built using a config file which is contructed by a scrapper which gathers the teams who will play and the point spread for the game. To contruct this config file once the web-app is running navigate to the proper url which the web-app is being ran from and go to /gen_config. Enter the number of games being played that week and optionaly add an image of encouragment or good luck to be displayed once picks are submitted. After these fields are subbmited you may now go back to the base url and should now see the updated table with the teams and spread for that week. (Note generating the config file needs to be done each week and this action will also erase the contents of the log file.)

### /admin_logs
There is a log directory which looks at the csv file of submitted picks and displays the picks in a table. Each time the page is loaded there is a call to espn api that gets the scores of active games and the table will autamatically highlight the cell of the winning picks. Below the table is a log which includes the name and timestamp of when each pick was submitted. There is also a toggle switch which turns on and off access to the /logs directory. 

### /logs
Similar to admin_logs in that it shows a table of submitted picks but does not show log containing the timestamp of submitted picks. If the /logs directory is accessed before the admin has allowed permision a message will show to return back once the first game starts. Once the admin has allowed access to this directory the table will appear with the same highlighted cells for each winning pick.  

## Example images
### example image of picks.html
![image of picks.html](https://github.com/rcobian11/FlaskNFL/blob/master/Images/picks_example.jpg)
### example image of logs and picks table
![image of logs.html](https://github.com/rcobian11/FlaskNFL/blob/master/Images/logs_example.jpg)

## TODO
- Change highlight condition from not pre to active or completed
- Look into making a possible manual config file version that can be used when games are rescheduled
