"""
TODO: THE VERTICALS CREATED ARE LIKE ALL OF THE TAGS, NOT JUST THE VERTICALS


python manage.py shell
exec(open('create_verticals.py').read())
"""

import pandas as pd
from tqdm import tqdm
import os
from data.models import Vertical, Tag, Company

BASE_PATH = ".\\outfiles\\tag_jsons"

verticals = pd.read_csv(os.path.join(BASE_PATH, "organized_tags.csv"))
verticals = verticals.drop("Nothing", axis=1) # Checked off but give no "vertical" information
clean = {}


for k in verticals:
    """
    SOMETHING ABOUT THE WAY THAT I AM PROCESSING THIS IS MAKING ALL THE TAGS INTO VERTICALS WHICH IS BAD
    
    """
    vertical, created = Vertical.objects.get_or_create(name=k)
    for i in range(len(verticals[k])):
        if isinstance(verticals[k][i], float):
            continue
        else:
            clean[verticals[k][i]] = k

for c in tqdm(Company.objects.all(), desc='Adding verticals to companies'):

    for t in c.tag_set.all():
        try:
            if clean[t.name] == "Irrelevant":
                c.relevant = False
                c.save()
                continue
            c.verticals.add(Vertical.objects.get(name=clean[t.name]))
        except KeyError:
            pass
        c.save()





