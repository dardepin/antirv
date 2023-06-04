import sys;
import json;
import base64;
import http.client

from config import *;

def get(connection:http.client.HTTPSConnection, action:str, creds:str, data:str = ""):
    
    status = 0; result = '';
    try:
        headers = { 'Authorization': 'Basic ' + creds };
        connection.request('GET', rv_url + '/v1/' + action, data, headers);

        response = connection.getresponse();
        status = response.status;
        result = response.read();
    except Exception as e:
        print('get():', sys.exc_info()[0]);

    return status, result;

def post(connection:http.client.HTTPSConnection, action:str, creds:str, data:str = ""):

    status = 0; result = '';
    try:
        headers = { 'Content-Type': 'application/json', 'Authorization': 'Basic ' + creds };
        connection.request('POST', rv_url + '/v1/' + action, data, headers);

        response = connection.getresponse();
        status = response.status;
        result = response.read();
    except Exception as e:
        print('post():', sys.exc_info()[0]);

    return status, result;

def info(connection:http.client.HTTPSConnection, creds:str):

    status, result = get(connection, 'deviceInfo', creds);
    if not status == 200:
        print('Can\'t get device info, get returned ' + str(status) + '\n');
        return False;
    else:
        print('Info ok: ' + rv_url + ':' + rv_port); 
        return True;

def config(connection:http.client.HTTPSConnection, creds:str):

    status, result = get(connection, 'config', creds);
    if not status == 200:
        print('Can\'t get device config, get returned ' + str(status) + '\n');
        return False;
    else:
        print('Config ok: ' + rv_url + ':' + rv_port); 
        return True;

def merge(connection:http.client.HTTPSConnection, creds:str):
    
    passwords = json.dumps({ "passwords": { "administrator": "111111", "operator": "222222" }});
    status, result = post(connection, 'mergeConfig', creds, passwords);
    if not status == 200 and not result == '1':
        print('Can\'t merge config, post returned ' + str(status) + '\n');
        return False;
    else:
        print('Merge ok: ' + rv_url + ':' + rv_port); 
        return True;

def reboot(connection:http.client.HTTPSConnection, creds:str):
    
    status, result = post(connection, 'reboot', creds);
    if not status== 200 and not result == '1':
        print('Can\'t reboot, post returned ' + str(status) + '\n');
        return False;
    else:
        print('Reboot ok: ' + rv_url + ':' + rv_port); 
        return True;

if __name__ == "__main__":

    try:
        creds = base64.b64encode((rv_user + ':' + rv_password).encode('ascii'));
        connection = http.client.HTTPSConnection(rv_url, rv_port);
    
        # skip info & config?
        if not info(connection, creds) or not config(connection, creds) or not merge(connection, creds): exit();
        else: reboot(connection, creds);
    except Exception as e:
        print('main():', sys.exc_info()[0]);
    finally:
        connection.close();
    exit();
    