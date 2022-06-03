#!/usr/bin/env python
# Download the latest or specified Paper JAR file
# Author: ChunkyFoil
# Email:  

import requests
import json
import hashlib
import os
import argparse


def get_latest_version(URL):
    res = requests.get(URL)
    return json.loads(res.text)['versions'][-1]


def get_latest_build(URL, version):
    res = requests.get(URL + 'versions/' + version)
    if not res.ok:
        raise Exception(res.text)
    return json.loads(res.text)['builds'][-1]


def get_jar_filename(URL, version, build):
    res = requests.get(URL + 'versions/' + version + '/builds/' + str(build))
    if not res.ok:
        raise Exception(res.text)
    return json.loads(res.text)['downloads']['application']


def main():
    parser = argparse.ArgumentParser(description='Download a Paper JAR file.  Default is latest')
    parser.add_argument('-v', '--version', help='version of Paper JAR to download')
    parser.add_argument('-b', '--build', help='build number of the JAR to download')
    args = parser.parse_args()

    URL = 'https://api.papermc.io/v2/projects/paper/'

    if args.version is None:
        args.version = get_latest_version(URL)
    if args.build is None:
        args.build = get_latest_build(URL, args.version)
    
    application = get_jar_filename(URL, args.version, args.build)
    name = application['name']
    sha = application['sha256']

    # download file
    print("Downloading " + name)
    res = requests.get(URL + 'versions/' + args.version + '/builds/' + str(args.build) + '/downloads/' + name)

    with open(name, 'wb') as file:
        file.write(res.content)

    # check SHA256 of downloaded file
    with open(name, 'rb') as file:
        jar_sha = hashlib.sha256(file.read()).hexdigest()

    if sha != jar_sha:
        keep = input("SHA256 mismatch: File may be corrupt.  Keep anyway? [y,N]: ")[:1].upper() or "N"
        if keep == "N":
            os.remove(name)


if __name__ == "__main__":
    main()