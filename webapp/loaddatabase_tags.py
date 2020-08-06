"""
Terminal Commands:
python manage.py shell
exec(open('loaddatabase_tags.py').read())
"""

import json
import os
from tqdm import tqdm
from data.models import Company, Tag
from django.utils.text import slugify

BASE_PATH = ".\\outfiles\\tag_jsons"


with open(os.path.join(BASE_PATH, "tags.json")) as f:
    data = json.load(f)
    if data is None:
        raise Exception("tag_jsons\{0} data is empty".format(f))
    for t in tqdm(data, desc="Loading tags into database"):
        tag, tag_create = Tag.objects.get_or_create(name=t)
        for c in data[t]:
            try:
                tag.companies.add(Company.objects.get(slug=slugify(c)))
            except:
                print("{0} does not exist, but it was in tags.json".format(c))
