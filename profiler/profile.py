import hashlib
import json
import os
import random
import time
import uuid
from string import ascii_letters

CHUNK_SIZE = 64 * 1024
KB = 1000
MB = 1000 * 1000
GB = 1000 * 1000 * 1000


def get_methods():
    """
    Returns a list of methods to use while hashing, along with
    constructers for the hashing algorithm
    """

    return [
        {
            "algorithm": "md5",
            "hasher": hashlib.md5()
        }, {
            "algorithm": "sha1",
            "hasher": hashlib.sha1(),
        }, {
            "algorithm": "sha2_224",
            "hasher": hashlib.sha224()
        }, {
            "algorithm": "sha2_256",
            "hasher": hashlib.sha256()
        }, {
            "algorithm": "sha2_384",
            "hasher": hashlib.sha384()
        }, {
            "algorithm": "sha2_512",
            "hasher": hashlib.sha512()
        }, {
            "algorithm": "sha3_224",
            "hasher": hashlib.sha3_224()
        }, {
            "algorithm": "sha3_256",
            "hasher": hashlib.sha3_256()
        }, {
            "algorithm": "sha3_384",
            "hasher": hashlib.sha3_384()
        }, {
            "algorithm": "sha3_512",
            "hasher": hashlib.sha3_512()
        }, {
            "algorithm": "blake2b",
            "hasher": hashlib.blake2b()
        }, {
            "algorithm": "blake2s",
            "hasher": hashlib.blake2s()
        }
    ]


def get_filesize(fp):
    size = os.stat(fp).st_size
    if size > GB:
        return f'{size/GB} GB'
    if size > MB:
        return f'{size/MB} MB'
    if size > KB:
        return f'{size/KB} KB'
    return f'{size} bytes'


def bulk_hash_file(fp):
    """
    Opens the file once and updates each hash with each chunk
    """
    methods = get_methods()

    the_file = open(fp, 'rb')
    chunk = the_file.read(CHUNK_SIZE)
    while chunk:
        for method in methods:
            method['hasher'].update(chunk)
        chunk = the_file.read(CHUNK_SIZE)

    results = {}
    for method in methods:
        results[method['algorithm']] = method['hasher'].hexdigest()
    return results


def calculate_individual(fp):
    """
    Opens the file once for each hash
    """

    results = {}
    methods = get_methods()

    for method in methods:
        the_file = open(fp, 'rb')
        chunk = the_file.read(CHUNK_SIZE)
        while chunk:
            method['hasher'].update(chunk)
            chunk = the_file.read(CHUNK_SIZE)
        results[method['algorithm']] = method['hasher'].hexdigest()
    return results


def profile_results(fp):
    """
    Hashes the file at the given path, calculating the time it takes to hash
    the file all at once, verses individually

    Returns the hashing results.
    """
    # Bulk
    start_time = time.time()
    bulk_results = bulk_hash_file(fp)
    bulk_results['elapsed_time'] = time.time() - start_time
    # Individual
    start_time = time.time()
    individual_results = calculate_individual(fp)
    individual_results['elapsed_time'] = time.time() - start_time
    return {
        "bulk_results": bulk_results,
        "individual_results": individual_results,
        "file_bytes": get_filesize(fp),
        "bulk_time_savings": individual_results['elapsed_time'] - bulk_results['elapsed_time'],
        "bulk_savings_percent": str(((individual_results['elapsed_time'] - bulk_results['elapsed_time'])/individual_results['elapsed_time'])*100)
    }


def generate_file(bytes):
    """
    Generates a file of a given number of bytes (characters) and
    returns the filepath... There are bound to be more efficient ways to do this,
    but I was going for quick and dirty here. Don't take this as a 'good' way of
    accomplishing this.
    """
    n = 0
    fname = f"samples/{uuid.uuid4()}.txt"
    with open(fname, 'w') as tmp_file:
        while n < bytes:
            tmp_file.write(random.choice(ascii_letters))
            n += 1
    return fname


def init(rounds=1):
    paths = []
    if not os.path.exists('samples'):
        os.makedirs('samples', exist_ok=True)
        paths = [
            generate_file(5*KB),
            generate_file(50*KB),
            generate_file(5*MB),
            generate_file(50*MB),
            generate_file(200*MB),
            generate_file(1*GB),
            generate_file(2*GB)
        ]
    else:
        for file_name in os.listdir('samples'):
            paths.append(os.path.join('samples', file_name))
    results = []
    for fp in paths:
        fp = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            fp
        )
        rounds_completed = 0
        while rounds_completed < rounds:
            results.append(profile_results(fp))
            rounds_completed += 1

    if rounds == 1:
        with open('comparison.json', 'w') as comparison_file:
            comparison_file.write(json.dumps(results, indent=2))
    else:
        bulk_time = 0
        individual_time = 0
        for result in results:
            bulk_time += result.get('bulk_results', {}).get('elapsed_time', 0)
            individual_time += result.get('individual_results',
                                          {}).get('elapsed_time', 0)
        with open('rounds.json', 'w') as comparison_file:
            comparison_file.write(json.dumps({
                "rounds": rounds,
                "individual_time": individual_time,
                "bulk_time": bulk_time,
                "savings": individual_time - bulk_time,
                "percent_savings": str(((individual_time - bulk_time) / individual_time) * 100)
            }, indent=2))


if __name__ == '__main__':
    init(5)
