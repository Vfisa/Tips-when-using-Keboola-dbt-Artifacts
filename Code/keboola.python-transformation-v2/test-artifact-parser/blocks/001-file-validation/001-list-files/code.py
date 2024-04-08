import os
import tarfile 

startpath = "/data/in/files/"
endpath = "/data/out/tables/"
endpath_files = "/data/out/files/"

def list_files(startpath):
    print("-------------")
    print("Listing directory: {}".format(startpath))
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))
    print("-------------")

list_files(startpath)

