import os
import hashlib
import shutil
import filetype
import time


def compute_hashes(fp):
    """
    Computes the hashes, and returns a tuple of MD5, SHA1
    """
    md5_hasher = hashlib.md5()
    sha1_hasher = hashlib.sha1()

    with open(fp, 'rb') as the_file:
        buffer = the_file.read()
        md5_hasher.update(buffer)
        sha1_hasher.update(buffer)
    the_file.close()

    return md5_hasher.hexdigest(), sha1_hasher.hexdigest()


def copy_file(fp, hash, hash_type):
    """
    Copies the file to the appropriate directory
    Uses the beautiful filetype library to guess filetype and append
    """
    kind = filetype.guess(fp)
    fname = hash
    if kind is not None:
        fname = f"{hash}.{kind.extension}"
    shutil.copyfile(
        fp,
        os.path.join('samples', hash_type, fname)
    )


def setup_dirs():
    """
    Setup the Directories

    samples/
        hashme/ # Place the files you want to hash in here
        md5/ # Files from to-hash will be placed here
        sha1/ # Files from to-hash will be placed here
    """
    this_dir = os.path.dirname(__file__)

    hash_dir = os.path.join(this_dir, 'samples', 'hashme')

    os.makedirs(hash_dir, exist_ok=True)
    os.makedirs(os.path.join(this_dir, 'samples', 'md5'), exist_ok=True)
    os.makedirs(os.path.join(this_dir, 'samples', 'sha1'), exist_ok=True)
    return hash_dir


def list_files(dir):
    """
    Lists the files in the 'hashme' dir that we're going to calculate hashes on
    """
    new_files = []
    for dirpath, dirnames, filenames in os.walk(dir):
        for fname in filenames:
            new_files.append(os.path.join(dirpath, fname))
    return new_files


def init():
    start_time = time.time()
    hash_dir = setup_dirs()
    files = list_files(hash_dir)
    for fp in files:
        md5, sha1 = compute_hashes(fp)
        copy_file(fp, md5, 'md5')
        copy_file(fp, sha1, 'sha1')
    shutil.rmtree(hash_dir)
    os.makedirs(hash_dir, exist_ok=True)
    elapsed_time = time.time() - start_time

    print(f"Elapsed Time: {elapsed_time}")


if __name__ == '__main__':
    init()
