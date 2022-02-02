import geopandas as gp
import matplotlib.pyplot as plt
import folium
import pandas
from shapely.geometry import Point, LineString, Polygon
import numpy as np




def extractingCoordinatesFromDataset(dataset_path,numberOfBreakPoint,bBox=None):
    ptrDataset = open(dataset_path)
    mainArray = []
    count = 0

    for eachLine in ptrDataset:
        if numberOfBreakPoint == count:
            print("BREAK POINT")
            break
        withoutNewLine = eachLine.split("\n")
        newList = withoutNewLine[0].split(";")
        floatLatitude = float(newList[3])
        floatLongitude = float(newList[4])
        if box[0]<floatLatitude<box[2] and box[1]<floatLongitude<box[3]:
            mainArray.append(newList)
        count += 1

    df = pandas.DataFrame(data=mainArray,columns=["Source_ID","Date","Altitude","Latitude","Longitude","Speed","Angle"])

    return df, mainArray

pointDict = dict()

box = (39.878259,32.774105,39.918492,32.851095) ## for points

bbox = (
    32.774105 , 39.878259, 32.851095 ,39.918492 ## for lineStrings
)

df, mainArray = extractingCoordinatesFromDataset("./Dataset/Trafik0701.txt",10000000,bBox=box)

print(df)
# print(mainArray)
# for (idx,row) in df.iterrows():
#     # print(row["Source_ID"])
#     floatLatitude = float(row["Latitude"])
#     floatLongitude = float(row["Longitude"])
#     if box[0]<floatLatitude<box[2] and box[1]<floatLongitude<box[3]:
#         newPoint = Point(floatLatitude, floatLongitude)
#         pointDict[newPoint] = row


roads = gp.read_file("ShapeFiles/gis_osm_roads_free_1.shp",bbox=bbox)

# print(roads)
roadsArray = roads.to_numpy().tolist()
# print(roads.columns)

count = roads.__len__()
coordinatesByIndex = []

for index in range(0,count):
    coordinatesByIndex.append(list(roads["geometry"][index].coords))

newSystem = []
newPolygons = [] #polygon with the same index id with lineStrings

for coords in coordinatesByIndex:
    newCoordinateSystem = [(b, a) for (a, b) in coords]
    newLineString = LineString(newCoordinateSystem)
    tmp = newLineString.buffer(0.01)
    newPolygons.append(tmp)
    newSystem.append(newCoordinateSystem)

# print("TEST CASE 1")
# print(len(coordinatesByIndex) == len(newPolygons))

# print("TEST CASE 2")
# print(len(roads) ==  len(newPolygons))

# print(newPolygons[0])

# relatedItems = dict()

# for key,value in pointDict.items():
#     # print(key)
#     # print(value)
#     index = 0
#     for eachPolygon in newPolygons:
#         if eachPolygon.contains(value):
#             print(value)
#             print("Related items found")
#             print(eachPolygon)
#             relatedItems[key] = index
#             break
#         index+=1
#
# print(relatedItems)

resultArray = []




for eachGps in mainArray:
    newPoint = Point(float(eachGps[3]),float(eachGps[4]))
    index = 0
    newRow = []
    flat_list = []
    for eachPolygon in newPolygons:
        if eachPolygon.contains(newPoint):
            newRow.append(eachGps)
            newRow.append(roadsArray[index])
            for each in newRow:
                for item in each:
                    flat_list.append(item)
            resultArray.append(flat_list)
            break
        index += 1

#
# print(resultArray)
# print(len(resultArray))

resultantDataFrame = pandas.DataFrame(data=resultArray,columns=["Source_ID","Date","Altitude","Latitude","Longitude","Speed","Angle",'osm_id', 'code', 'fclass', 'name', 'ref', 'oneway', 'maxspeed',
        'layer', 'bridge', 'tunnel', 'geometry'])

print(resultantDataFrame)

resultantDataFrame.to_csv("result.csv")

m = folium.Map(location=[39, 35], zoom_start=10)

for coords in newSystem:
    my_PolyLine=folium.PolyLine(locations=coords,weight=3)
    m.add_child(my_PolyLine)

m.save('line_example.html')

roads.plot()
plt.savefig("roads.jpg")




## ['osm_id', 'code', 'fclass', 'name', 'ref', 'oneway', 'maxspeed',
       # 'layer', 'bridge', 'tunnel', 'geometry']
