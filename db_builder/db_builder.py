from cs50 import SQL
from helpers import region_check, program_stream_check, validate
import csv

db = SQL("sqlite:///jobs.db")
sn = 0
with open("lmiaQ3.csv","r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        sn += 1
        if validate(row) == False:
            continue
        employer = row["Employer"]
        # If the employer is not in the employers table, put the employer
        employer_data = db.execute("SELECT * FROM employers WHERE company=?;", employer)
        if not employer_data:
            db.execute("INSERT INTO employers(company) VALUES(?);", employer)

        occupation = row["Occupation"].split("-")
        number = int(occupation[0])
        name = "".join(occupation[1:])
        # If the occupation is not in the occupatios table, put the occupation
        occupation_data = db.execute("SELECT * FROM occupations WHERE name=? AND number=?;", name, number)
        if len(occupation_data) < 1:
            db.execute("INSERT INTO occupations(name, number) VALUES(?, ?);", name, number)

        location = row["Address"]
        # If the location is not in the locations table, put it
        location_data = db.execute("SELECT * FROM locations WHERE address=?;", location)
        if not location_data:
            db.execute("INSERT INTO locations(address) VALUES(?);", location)

        region = region_check(row["Province/Territory"].strip())
        program_stream = program_stream_check(row["Program Stream"].strip())
        approved_position = row["Approved Positions"]
        approved_lmia = row["Approved LMIAs"]
        employer_id = db.execute("SELECT * FROM employers WHERE company=?", employer)[0]["id"]
        occupation_id = db.execute("SELECT * FROM occupations WHERE name=? AND number=?;", name, number)[0]["id"]
        location_id = db.execute("SELECT * FROM locations WHERE address=?;", location)[0]["id"]

        # Fill the fourth table ie the jobs table. Ignore the users and user_jobs table for now
        db.execute('''INSERT INTO jobs
                   (employer_id, occupation_id, location_id, region, program_stream, approved_position, approved_lmia)
                   VALUES(?, ?, ?, ?, ?, ?, ?);''',
                   employer_id, occupation_id, location_id, region, program_stream, approved_position, approved_lmia)
        print(sn)
