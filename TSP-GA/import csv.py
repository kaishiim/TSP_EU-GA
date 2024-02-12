import csv
def putfloat(x):
    return str(x).replace(".", ',')

with open('country-capital-lat-long-population.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    header = next(reader)
    print(header)
    rows = []
    for row in reader:
        #print(row)
        print(row[1:4])
        rows.append([row[1], float(row[2]), float(row[3]), int(row[4])])
print(rows)
lat_min,lat_max = 37, 72
long_min, long_max = -25, 39
pop_min = 5E4
h1 = header[1:5]
r1 = [r for r in rows if (long_min <= r[2] <= long_max) and (lat_min <= r[1] <= lat_max) and (pop_min <= r[3]) and r[0] != 'Ankara']
#r2 = [r for r in rows if (long_min <= r[2] <= long_max) and (lat_min <= r[1] <= lat_max) and (pop_min > r[3])]

print("r1 =", r1)
print(len(r1))

with open('capitals.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(h1)
    for r in r1:
        writer.writerow([r[0], putfloat(r[1]), putfloat(r[2]), r[3]])

"""
Lattitudes 37°N to 72°N  and the longitudes 25°W to 65°E.
Fundet på https://www.toppr.com/ask/question/the-latitudinal-extent-of-europe-is/
"""
