## Introduction
For GIT (Github) testing only! AntiRV is a simple Python tool for automatic changing default pin codes for RV 3.0 devices.
## Current Releases
__0.1__ - Initial commit. I've no access to RV now, so, this code was mostly theoretical ;)<br />
__0.2__ - Auth fixed. Logging, bruteforce functions are available;
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

Other settings: <br/>
* __rv_brute__ - Try to bruteforce admin password. Not testted yet; <br />
* __rv_log__ - You can specify file to log. May be extra-useful with __v_random__ opion; <br />
* __rv_random__ - setup new random pin codes for admin and operator; Better use __rv_log__ option with in to know new pin codes; <br />
## Plans for future releases
* Add more types of RV devices (2.0?);
* Scan local network area for RV devices; <br />
* Test bruteforce pin function for RV devices where the password was changed;<br />
## Licenses
Use and modify on your own risk.
