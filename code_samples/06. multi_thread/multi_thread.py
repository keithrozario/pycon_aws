import math
import logging
from multiprocessing import Process, Pipe
from random import randint
from datetime import datetime
import boto3

logger = logging.getLogger()
level = logging.INFO

def gen_items(num_items):

    pk = datetime.now().isoformat()
    rk = randint(1, 100000000)

    results = []
    for i in range(num_items):
        results.append({'pk': {'S': pk},
                        'rk': {'N': str(rk)}})
    return results


def write_items(items, conn):

    """
    Receives a list of text to be processed, one element per row
    Returns a list of dictionaries to be combined into a single file
    """
    dynamo_client = boto3.client('dynamodb')
    responses = []

    for item in items:

        responses.append(item)

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

    items = gen_items(100)
    results = multiproc_requests(items, 2, write_items)

   

