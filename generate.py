import os
import sys
import tempfile
from multiprocessing import Pool
from pathlib import Path
from subprocess import check_call

import requests

EVENT_ID = "IY75fFIx7257tFDBa4yp"

SHEET = """
sheet(
  org: "{org_name}",
  team: "{team_name}",
  number: "{team_number}",
  rooms: (
    exam: "{exam_room}",
    awards: "{awards_room}",
  ),
  students: {students},
),
"""

AWARDS = {
    ("A", "C"): "Dwinelle 145",
    ("C", "Re"): "Dwinelle 155",
    ("Re", "Z"): "Hearst Field Annex A1",
}

SESSION = requests.Session()
SESSION.headers = {"Authorization": f"Bearer {os.environ['CONTESTDOJO_API_KEY']}"}


def make_sheet(number):
    team_req = SESSION.get(
        f"https://api.contestdojo.com/events/{EVENT_ID}/teams/?number={number}"
    )
    team_req.raise_for_status()
    try:
        team_data = team_req.json()[0]
    except IndexError:
        raise ValueError(f"Team {number} not found")

    org_req = SESSION.get(
        f"https://api.contestdojo.com/events/{EVENT_ID}/orgs/{team_data['org']}"
    )
    org_req.raise_for_status()
    org_data = org_req.json()

    students_req = SESSION.get(
        f"https://api.contestdojo.com/events/{EVENT_ID}/students/?team={team_data['id']}"
    )
    students_req.raise_for_status()
    students_data = students_req.json()

    students = "\n".join(
        f'(number: "{student["number"]}", name: "{student["fname"]} {student["lname"]}"),'
        for student in students_data
    )

    for (s, e), awards_room in AWARDS.items():
        if s <= org_data["name"] <= e:
            break

    return SHEET.format(
        org_name=org_data["name"],
        team_name=team_data["name"],
        team_number=team_data["number"],
        exam_room=team_data["checkInPool"],
        awards_room=awards_room,
        students=f"({students})",
    )


if __name__ == "__main__":
    numbers = input("Team #s: ").replace(",", " ").split()
    # sheets = [make_sheet(team) for team in numbers]
    with Pool() as pool:
        sheets = pool.map(make_sheet, numbers)
    sheets = "\n\n".join(sheets)

    typst_code = f"""
        #import "template.typ": wrapper, sheets, sheet
        #wrapper(sheets(
            {sheets}
        ))
    """

    fd, filename = tempfile.mkstemp("w", dir=Path())
    fp = open(fd, "w")
    fp.write(typst_code)
    fp.close()

    check_call(["typst", "compile", filename, "output.pdf"])
    os.remove(filename)
