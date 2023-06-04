## Introduction
For GIT (Github) testing only! AntiRV is a simple Python tool for automatic changing default pin codes for RV 3.0 devices.
## Current Releases
__0.1__ - Initial commit.<br />
## Platforms
Any Linux or Windows. `Python3` and `request` library required. <br />
## Usage
Rename `default_config.py` to `config.py`, provide your ip, port, usernames, pins and
just launch it! <br />
Typical launch:
> *python antirv.py*

or
> *python3 antirv.py*
## Config file
Configure setting in config.py: <br />
* __rv_url__ is valid url for RV; <br />
* __rv_port__ is valid port (int) for RV; <br />
* __rv_user__ is an admin username for RV; <br />
* __rv_password__ is admin pin code for RV; <br />
## Plans for future releases
* Randomize option for new pins (use carefully);
* Add more types of RV devices (2.0?);
* Add logging;
* Scan local network area for RV devices; <br />
* Bruteforce pin for RV devices where the password was changed;<br />
## Licenses
Use and modify on your own risk.
