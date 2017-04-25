# DATA CHANGE MONITORING AND ALERTING 
TEAM 190 TXKKIU

## RELEASE NOTES

### New Features
History database to keep track of transactions.

History database can be queried by number of most recent queries and by date range(s).

Keys can be deemed important through matching a regex pattern.

Regex can be configured in a file, pairing regex(es) to email addresses so that users are alerted when a particular matching key is changed.

Web server wrapper around primary key-value store to ensure it can be queried using a restful API through web browser, terminal, or any modern programming language.

Separation of main application, history database implementation, key-value store implementation and configuration implementation to allow easy changes to any component without disrupting the system as a whole.

Integration Proof of Concept using LDAP queries on GTED/GTAD with configurable scheduling

### Bug Fixes
As we created a new implementation from the ground up, no bugs in the previous implementation were encountered nor fixed.

### Known Bugs and Defects
At the time of writing, there are no known bugs or defects in our implementation. 


## INSTALLATION GUIDE

### Pre-requisites
mongodb, python, java, and pip need to be installed on the host machine for this application to run. 

### Dependent Libraries
Python libraries:
Run `pip install -r requirements.txt`
This will install all python-related dependencies through pip

Web Server:
Navigate to: https://github.com/koek67/rocks-db-server
download the files and follow the build instructions below for the web server.

### Download Instructions 
The necessary files can be cloned or downloaded from this repository

### Build Instructions
To build the web server, first navigate to the web server directory in a terminal
Run: `./gradlew build`


### Installation of Application
Once the web server is built and running, only the configuration files need to be set. This includes specifying regexes for keys that are deemed important and emails to be alerted when said keys are changed and timing information for integration scheduling

### Run Instructions
After building the rocks db server, run the history tracker application with `python main.py` and you will be presented with a REPl to access the history logs. For instructions on what commands are available, type `help`.

