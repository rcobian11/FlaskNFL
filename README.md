# NFL Picks
Web app which gets picks from user and stores selection in a csv file. Python Flask backend html/js front end(Looking to incorporate angularJS).

## usage
### AWS ElasticBeanstalk (Production)
If deployed to AWS Elastic Beanstalk Production version will be ran and picks.csv will be stored in aws S3 bucket.

### Local (Development)
```bash
pip install -r requirments.txt
```
If ran locally (using flask run or python application.py) development version will be ran and picks.csv will be stored locally in same directory.

## TODO
- Look into adding password to gen_config directory
- Check for multiple entries and use only the latest one
- Make seperate html file to be rendered when picks are submitted 