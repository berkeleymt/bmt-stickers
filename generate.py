import os
import sys
import tempfile
from pathlib import Path
from subprocess import check_call

import requests

EVENT_ID = "3tAOVBMVF5KInjMIHp0R"

SHEET = """
#sheet(
  org: "{org_name}",
  team: "{team_name}",
  number: "{team_number}",
  rooms: (
    power: "{power_room}",
    guts: "{guts_room}",
    awards: "{awards_room}",
  ),
  students: {students},
)
"""

AWARDS_DWINELLE_145 = {
    "ar8cJSArZ5P2cSstO78w",
    "lI2FYvPdAlRqN098FLBr",
    "r8IQdZlEZ1rDvrRCEIBR",
    "5tQWdEHW9aBC1mZ8dBfE",
    "fXyxweZJsTnISQseSXhr",
    "e1mm0BLo1G6UnAyte5Tw",
    "CkyzuKre4VIT7pltGLyj",
    "NDSyHT2K6vkkXtD5d0qv",
    "2DZYstMox830PYxGoYZ5",
    "cjFRU5YxcaSl4N1P6phX",
    "OBZBUMt3RCdUld4T3Oli",
    "8KJeCQPaknYoFLEMTHs3",
    "X6M65di7Dm5p5iQhVrmP",
    "ijZR7mVr1ClTsx3Hrtxa",
    "6hHPLebHPVoNBEVoQAyV",
    "h6Ncdgtxvx2XZ09H3mGC",
    "SYM8zPeh9F6MVQTz9ejD",
    "HdQQrzP0RHBr39iovqQu",
    "wMmBNEEArJSe3L6asrId",
    "8eAzIBDcLu5MDHaR5Heu",
    "gP7eoEtC0juTiJ5E6KtB",
    "fa4CsVK5FO2sjFf0fiTQ",
    "qmPujuqTdvAUdIjC9IGT",
    "BBMA4JOdTXExxZ2kl6bF",
}

SESSION = requests.Session()
SESSION.headers = {"Authorization": f"Bearer {os.environ['CONTESTDOJO_API_KEY']}"}


def make_sheet(number):
    team_req = SESSION.get(f"https://api.contestdojo.com/events/{EVENT_ID}/teams/?number={number}")
    team_req.raise_for_status()
    try:
        team_data = team_req.json()[0]
    except IndexError:
        raise ValueError(f"Team {number} not found")

    org_req = SESSION.get(f"https://api.contestdojo.com/events/{EVENT_ID}/orgs/{team_data['org']}")
    org_req.raise_for_status()
    org_data = org_req.json()

    students_req = SESSION.get(f"https://api.contestdojo.com/events/{EVENT_ID}/students/?team={team_data['id']}")
    students_req.raise_for_status()
    students_data = students_req.json()

    students = "\n".join(
        f'(number: "{student["number"]}", name: "{student["fname"]} {student["lname"]}"),' for student in students_data
    )

    return SHEET.format(
        org_name=org_data["name"],
        team_name=team_data["name"],
        team_number=team_data["number"],
        power_room=team_data["checkInPool"],
        guts_room="TBD",
        awards_room="Dwinelle 145" if org_data["id"] in AWARDS_DWINELLE_145 else "Dwinelle 155",
        students=f"({students})",
    )


if __name__ == "__main__":
    numbers = input("Team #s: ").replace(",", " ").split()
    sheets = "\n\n".join(make_sheet(team) for team in numbers)

    typst_code = f'#import "template.typ": sheet\n\n{sheets}'

    fd, filename = tempfile.mkstemp("w", dir=Path())
    fp = open(fd, "w")
    fp.write(typst_code)
    fp.close()

    check_call(["typst", "compile", filename, "output.pdf"])
    os.remove(filename)
