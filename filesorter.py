from distutils import extension
import json
import os
import pathlib
from urllib.parse import SplitResult


scanlocations=[str]
sortpaths=[]

with open("./configs.json") as f:
    data = json.load(f)

    scanlocations=data["scanlocations"]
    sortpaths=data["sortpaths"]

class Sort:
    path:str
    extensions:list[str]
    filepaths = list[str]

    def __init__(self,path:str,extensions:list[str]):
        self.path = path
        self.extensions = extensions
        self.filepaths = []
        try:
            os.makedirs(path)
        except FileExistsError:
            pass

def scanAndSort(path:str):
    filelist = []
    sps = []

    for sortpath in sortpaths:   
        sps.append(Sort(sortpath["destination"],sortpath["fileextensions"]))



    for root, dirs, files in os.walk(path):
        for file in files:
            filelist.append(os.path.join(root,file))
        break

    for file in filelist:
        extension = pathlib.Path(file).suffix
        extension = extension.strip('.')
        other = True
        for sp in sps:
            if extension in sp.extensions:
                other = False
                sp.filepaths.append(file)

        if other == True:
            for s in sps:
                if '*'in s.extensions:
                    s.filepaths.append(file)   
    
    for sp in sps:
        for f in sp.filepaths:
            filename = os.path.basename(f)
            os.replace(f,os.path.join(sp.path,filename))


for location in scanlocations:
    scanAndSort(location)

