"""
Terminal Commands:
python manage.py shell
exec(open('loaddatabase_tags.py').read())
"""

import json
import os
from tqdm import tqdm
from database_interface.models import Company, Investor, Tag

BASE_PATH = ".\\outfiles\\"


with open(os.path.join(BASE_PATH, "tag_jsons\\tags.json")) as f:
    issues = []
    data = json.load(f)
    if not data:
        raise Exception("tag_jsons\{0} data is empty".format(f))
    for t in tqdm(data, desc="Loading tags into database"):
        tag, tag_create = Tag.objects.get_or_create(name=t)
        for c in data[t]:
            tag.companies.add(Company.objects.get(name=c))
