"""
Terminal Commands:
python manage.py shell
exec(open('loaddatabase_companies.py').read())
"""

import json
import os
from tqdm import tqdm
from database_interface.models import Company, Investor, Tag

BASE_PATH = ".\\outfiles\\"

for file in os.listdir(os.path.join(BASE_PATH, "company_jsons")):
    investor_name = os.path.splitext(file)[0]
    with open(os.path.join(BASE_PATH, "company_jsons", file)) as f:
        data = json.load(f)
        if not data:
            raise Exception("company_jsons\{0} data is empty".format(f))
        investor, inv_create = Investor.objects.get_or_create(name=investor_name)  # file minus the .json?
        for c in tqdm(data, desc="Loading companies into database for {}".format(investor_name)):
            if not c:
                continue
            company, created = Company.objects.get_or_create(name=c["name"])


            #if not created: # if updating an existing value
            for field in Company._meta.get_fields():
                if field.name == "tag":
                    continue
                if field.name == "investors":
                    company.investors.add(Investor.objects.get(name=investor_name))

                try:
                    if (not getattr(company, field.name)) and c[field.name]:
                        setattr(company, field.name, c[field.name])
                except KeyError:
                    pass
            company.investors.add(investor)
            company.save()
