import math
import logging
from multiprocessing import Process, Pipe
from datetime import datetime
import boto3
import time

logger = logging.getLogger()
level = logging.INFO

ssm_client = boto3.client('ssm')
table_name = ssm_client.get_parameter(Name='/pycon/dynamodb_table_name')['Parameter']['Value']


def main(event, context):

    num_items = event.get('num_items', 100)
    num_procs = event.get('num_proc', 2)

    result = start(num_items, num_procs)

    return result


def start(num_items, num_procs):

    items = gen_items(num_items)
    response = multiproc_requests(items, num_procs, write_items)

    return response


def start_compute(event, context):

    items = ['password', 'password1', 'password2', 'password3']
    response = multiproc_requests(items, 2, calc_items)

    return response


def gen_items(num_items):

    pk = datetime.now().isoformat()
    ttl_value = int(time.time() + 8*3600)

    results = []

    for i in range(num_items):
        results.append({'pk': {'S': pk},
                        'rk': {'N': str(i)},
                        'expires_in': {'N': str(ttl_value)}})
    return results


def write_items(items, conn):

    """
    Receives a list of text to be processed, one element per row
    Returns a list of dictionaries to be combined into a single file
    """
    dynamodb_client = boto3.client('dynamodb')
    responses = []

    for item in items:
        response = dynamodb_client.put_item(TableName=table_name,
                                            Item=item)
        responses.append(response)

    conn.send(responses)
    conn.close()


def calc_items(items, conn):

    import hashlib, binascii,os

    responses = []

    for password in items:
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                      salt, 1000000)
        pwdhash = binascii.hexlify(pwdhash)
        responses.append((salt + pwdhash).decode('ascii'))

    conn.send(responses)
    conn.close()


def multiproc_requests(items, proc_count, func):
    logger.debug('Spawning {} processes'.format(proc_count))

    per_proc = int(math.ceil(len(items) / proc_count))

    # create a list to keep all processes
    processes = []

    # create a list to keep connections
    parent_connections = []

    # create a process per instance
    for count in range(proc_count):
        # create a pipe for communication
        parent_conn, child_conn = Pipe()
        parent_connections.append(parent_conn)

        # create the process, pass instance and connection
        sub_list = [x for x in items[count * per_proc: (count + 1) * per_proc]]
        process = Process(target=func, args=(sub_list, child_conn,))
        processes.append(process)

    logger.debug("Making Requests for {} rows".format(len(items)))
    # start all processes
    for process in processes:
        process.start()

    logger.debug("Processes Started, waiting for closed connections")

    responses = []
    logger.debug("Reading info")
    for parent_connection in parent_connections:
        responses.extend(parent_connection.recv())

    for process in processes:
        process.join()

    return responses


if __name__ == '__main__':
    #
    # items = gen_items(100)
    # results = multiproc_requests(items, 2, write_items)

    items = ['password', 'password2', 'password3', 'password4']
    results = multiproc_requests(items, 2, calc_items)
    print(results)



