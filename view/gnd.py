#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Creator:          D. Herre
GitHub:   haldru/Reske2015

Created:        2020-08-11
Last Modified:  2020-08-11
"""
import os

from librair import schemas
from librair import services

entities = schemas.json.reader("data/gnd.json")

if not os.path.exists("view/output"):
    os.mkdir("view/output")

person_data = {}
corporate_data = {}

print("RESKE (2015)")
print("")
print("")
print("RETRIEVE DATA...")
for gnd in entities:
    gnd_data = services.entityfacts.request(gnd)
    if "@type" in gnd_data:
        if gnd_data["@type"] == "person":
            person_data[gnd] = gnd_data
        elif gnd_data["@type"] == "organisation":
            corporate_data[gnd] = gnd_data
        else:
            print("unhandled entity type: ", gnd_data["@type"])
    else:
        print("could not find type of entity with id: ", gnd)


print("")
print("")
print("PERSON")
print("")
print("GND-NR.", "NAME", "GEBURTSDATUM", "STERBEDATUM", "WIRKUNGSORT", "WIRKUNGSZEITRAUM")
for gnd in person_data:
    person = person_data[gnd]
    full_name = person["preferredName"] if "preferredName" in person else ""
    date_birth = person["dateOfBirth"] if "dateOfBirth" in person else ""
    date_death = person["dateOfDeath"] if "dateOfDeath" in person else ""
    # place_birth = person["placeOfBirth"] if "placeOfBirth" in person else []
    # place_death = person["placeOfDeath"] if "placeOfDeath" in person else []
    place_activity = person["placeOfActivity"] if "placeOfActivity" in person else []
    place_activity = " | ".join([pa['preferredName'] for pa in place_activity])
    period_activity = person["periodOfActivity"] if "periodOfActivity" in gnd_data else ""
    print(gnd, full_name, date_birth, date_death, place_activity, period_activity)


schemas.json.writer(person_data, "view/output/person.json")


if corporate_data:
    print("")
    print("")
    print("ORGANISATION")
    print("")
    print("GND-NR.", "NAME", "WIRKUNGSORT", "WIRKUNGSZEITRAUM")
    for gnd in corporate_data:
        corporate = corporate_data[gnd]
        full_name = corporate["preferredName"] if "preferredName" in corporate else ""
        place_business = corporate["placeOfBusiness"] if "placeOfBusiness" in corporate else []
        place_business = " | ".join([pb['preferredName'] for pb in place_business])
        start_business = ";".join(corporate["dateOfEstablishment"] if "dateOfEstablishment" in corporate else [""])
        end_business = ";".join(corporate["dateOfTermination"] if "dateOfTermination" in corporate else [""])
        print(gnd, full_name, place_business, start_business, end_business)
    schemas.json.writer(corporate_data, "view/output/organisation.json")
