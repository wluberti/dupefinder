#! /usr/bin/env python3
# dupFinder.py

"""
    Based on: https://www.pythoncentral.io/finding-duplicate-files-with-python/
"""
import os, sys
import hashlib

def findDup(parentFolder):
    # Dups in format {hash:[names]}
    dups = {}
    for dirName, subdirs, fileList in os.walk(parentFolder):
        # print('Scanning %s...' % dirName)
        for filename in fileList:
            # Get the path to the file
            path = os.path.join(dirName, filename)

            # Calculate hash
            file_hash = hashfile(path)

            # Add or append the file path
            if file_hash in dups:
                dups[file_hash].append(path)
            else:
                dups[file_hash] = [path]
    return dups


# Joins two dictionaries
def joinDicts(dict1, dict2):
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]


def hashfile(path, blocksize = 65536):
    with open(path, 'rb') as afile:
        hasher = hashlib.sha1()
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
        return hasher.hexdigest()


def printResults(dict1):
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    if len(results) > 0:
        print('Duplicates Found:')
        print('The following files are identical. The name could differ, but the content is identical')
        for result in results:
            print('___________________')

            best = max(result, key=len)
            print(f"Best result to keep: {best}")

            for subresult in result:
                if (subresult != best):
                    print(f"deleting: {subresult}")
                    # try:
                    #     os.remove(subresult)
                    # except Exception as e:
                    #     print (f"{result} error: {e}")

    else:
        print('No duplicate files found.')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        dups = {}
        folders = sys.argv[1:]

        for i in folders:
            # Iterate the folders given
            if os.path.exists(i):
                # Find the duplicated files and append them to the dups
                joinDicts(dups, findDup(i))
            else:
                print('%s is not a valid path, please verify' % i)
                sys.exit()
        printResults(dups)
    else:
        print('Usage: python dupFinder.py folder or python dupFinder.py folder1 folder2 folder3')
