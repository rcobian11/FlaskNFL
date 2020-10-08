# NFL Picks
Web app which gets picks from user and stores selection in a csv file. Python Flask backend html/js front end(Looking to incorporate angularJS).

## Usage
### AWS ElasticBeanstalk (Production)
If deployed to AWS Elastic Beanstalk Production version will be ran and picks.csv will be stored in aws S3 bucket.

### Local (Development)
```bash
pip install -r requirments.txt
```
If ran locally (using flask run or python application.py) development version will be ran and picks.csv will be stored locally in same directory.

### On first deployment and each new week the config file will need to be created/updated.

## Directories
### /gen_config
The web-app is built using a config file which is contructed by a scrapper which gathers the teams who will play and the point spread for the game. To contruct this config file once the web-app is running navigate to the proper url which the web-app is being ran from and go to /gen_config. Enter the number of games being played that week and optionaly add an image of encouragment or good luck to be displayed once picks are submitted. After these fields are subbmited you may now go back to the base url and should now see the updated table with the teams and spread for that week. (Note generating the config file needs to be done each week and this action will also erase the contents of the log file.)

### /admin_logs
There is a log directory which looks at the csv file of submitted picks and displays the picks in a table. Each cell in the table is clickable and will toggle green to indicate that the pick was correct. Below the table there is also a log containing the name and timestamp of when each pick was submitted. 

### /logs
Similar to admin_logs in that it shows a table of submitted picks but does not show log containing the timestamp of submitted picks. If the directory is accessed before the start of the first game of the weekend the page will show a message telling user to return after the start of the first game. Otherwise it will show the table as normal. 

## Example images
![image of picks.html](https://github.com/rcobian11/FlaskNFL/blob/master/Images/picks_example.jpg)
![image of logs.html](https://github.com/rcobian11/FlaskNFL/blob/master/Images/logs_example.jpg)

## TODO
- Scrap results of games and auto highlight correct picks in log table
- Get average spread from all avaliable and average them out
