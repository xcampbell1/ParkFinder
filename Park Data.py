import sqlite3, os
choice = input("Do you wish to run live import and reset dbase? Y / N: ")
if choice.lower() == "y":
    try:
        if os.path.exists("database.db"):
            os.remove("database.db")
        import csv
        db = sqlite3.connect("database.db")
        db.cursor().execute("""
            CREATE TABLE parks(
                X TEXT,
                Y TEXT,
                OBJECTID INTEGER PRIMARY KEY UNIQUE,
                Description TEXT,
                ParkType TEXT,
                Car_Park TEXT,
                Dog_Off_Leash_Area TEXT,
                Electric_BBQ TEXT,
                Picnic_Set TEXT,
                Rubbish_Bins TEXT,
                Shelter TEXT,
                Toilets TEXT,
                Water_Fountain TEXT,
                Basketball_Court TEXT,
                Play_Equipment TEXT,
                Playground_Area TEXT,
                Skate_Park TEXT,
                Exercise_Equipment TEXT,
                Suburb TEXT,
                ADDRESS TEXT,
                APS TEXT,
                Rating INTEGER
            );
        """)
        csvfile = open('data_clean.csv') #https://stackoverflow.com/questions/50228008/strange-character-while-reading-a-csv-file
        data = csv.DictReader(csvfile)
        for park in data:
            query = "INSERT INTO parks VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)" #? are placeholders for fields in table
            rating = float(0)
            print(park)
            if park['Dog_Off_Leash_Area'] != "No":
                rating = rating + 0.5
            if park['Car_Park'] != "No":
                rating = rating + 0.5
            if park['Electric_BBQ'] != "No":
                rating = rating + 1
            if park['Picnic_Set'] != "No":
                rating = rating + 1.25
            if park['Rubbish_Bins'] != "No":
                rating = rating + 1.25
            if park['Shelter'] != "No":
                rating = rating + 1.25
            if park['Toilets'] != "No":
                rating = rating + 1.25
            if park['Water_Fountain'] != "No":
                rating = rating + 0.7
            if park['Basketball_Court'] != "No":
                rating = rating + 0.5
            if park['Play_Equipment'] != "No":
                rating = rating + 0.5
            if park['Playground_Area'] != "No":
                rating = rating + 0.5
            if park['Skate_Park'] != "No":  
                rating = rating + 0.5
            if park['Exercise_Equipment'] != "No":
                rating = rating + 0.3
            db.cursor().execute(query, (park['xx'],park['yy'],park['OBJECTID'],park['Description'],
                                        park['ParkType'],park['Car_Park'],park['Dog_Off_Leash_Area'],park['Electric_BBQ'],
                                        park['Picnic_Set'],park['Rubbish_Bins'],park['Shelter'],park['Toilets'],
                                        park['Water_Fountain'],park['Basketball_Court'],park['Play_Equipment'],park['Playground_Area'],
                                        park['Skate_Park'],park['Exercise_Equipment'],park['Suburb'],park['ADDRESS'],park['APS'],rating))
        db.commit()
    except Exception as e:
        print("Something bad happened:",e)
    finally:
        db.close()

############################################################################################################################

print("Welcome to SQL Query Engine")
print("Enter x to exit.")
print("---------------------------")
suburb = input("Enter suburb name >> ")
preferences = { 'Dog_Off_Leash_Area':'No', 'Car_Park':'No', 'Electric_BBQ':'No', 'Exercise_Equipment':'No', 'Dog_Off_Leash_Area':'No', 'Toilets':'No', 'Water_Fountain':'No',
                'Basketball_Court':'No', 'Play_Equipment':'No', 'Playground_Area':'No', 'Skate_Park':'No', 'Exercise_Equipment':'No'}

for p in preferences:
    a = input(p+"? Y/N:")
    preferences[p] = 'Yes' if a.upper() == 'Y' else 'No'


while suburb != 'x':
    try:
        db = sqlite3.connect("database.db")
        db.row_factory = sqlite3.Row #https://stackoverflow.com/questions/576933/how-can-i-reference-columns-by-their-names-in-python-calling-sqlite
        results =  db.cursor().execute("SELECT * FROM parks WHERE ADDRESS LIKE ? ORDER BY rating DESC", (f'%{suburb}%',)).fetchall() #https://stackoverflow.com/questions/20904209/how-to-execute-select-like-statement-with-a-placeholder-in-sqlite
        print( len(results), "records found.")
        for row in results:
            pref = ""
            for preference in preferences:
                if preferences[preference] == "Yes" and row[preference] == "Yes": #the preference matches the park!
                    pref = pref + " Found: " + preference + ","
            print(row['ADDRESS'],"  Rating:", row['Rating'],"/ 10", pref + " " )
            
    except Exception as e:
        print("Something bad happened:",e)
    finally:
        db.close()
    print("---------------------------")
    suburb = input("Enter suburb name >> ")
#Add Url Output
#base url = https://www.google.com/maps/search/
#e.g https://www.google.com/maps/search/122-188 SUMMERFIELDS DRIVE CABOOLTUREthub
