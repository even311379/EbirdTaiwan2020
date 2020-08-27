# import shapefile
# import random
# import pandas as pd
# from pyproj import Transformer



# # all shp related files should stay in one folder

shp_file = 'TOWN_MOI_1090727.shp'

# # transformer = Transformer.from_crs(3826, 4326)
# # ignore potential geocodex issue for now

# sf = shapefile.Reader(shp_file)

# gstring_head = '{"type": "FeatureCollection","features": ['
# gstring_content_template = '{"type": "Feature","properties": {"Name":"{NAME}", "IDS":"{ID}", "geometry": {"type": "MultiPolygon","coordinates": [{POINTS}]}}},'
# gstring_tail = ']}'

# def RandomHexColor():
#     s = '0123456789abcdef'
#     o = '#'
#     for i in range(6):
#         o+=s[random.randint(0,15)]
#     return o

# gstring_content = ''

# Names = []
# IDS = []
# L = 5
# for i in range(L):
#     Name = f'{sf.record(i)[2]}, {sf.record(i)[3]}'
#     ID = i
#     # points = [list(transformer.transform(p[1],p[0])) for p in sf.shape(0).points]
#     points = [list(p) for p in sf.shape(i).points]
#     Names.append(Name)
#     IDS.append(ID)
#     t = gstring_content_template
#     t = t.replace('{NAME}', Name)    
#     t = t.replace('{ID}',str(ID))
#     t = t.replace('{POINTS}',str(points))
#     if i == L -1:
#         t = t.replace(']}}},', ']}}}')
#     gstring_content += t

# with open('helper_files/TaiwanCounties.geojson', 'w+') as f:
#     f.write(gstring_head + gstring_content+gstring_tail)

# D = []
# for i in range(len(IDS)):
#     D.append(random.randint(0, 30))

# pd.DataFrame(dict(IDS=IDS, Day1=D, Name=Names)).to_csv('helper_files/TestMapData.csv', index=False)


'''
After waste bunch of time, simply use geopandas to convert shp to geojson is most easy
and correct way....

My manual code missed lots of brackets ... and just not work....

'''

import geopandas
myshpfile = geopandas.read_file(shp_file, encoding='utf8')


# convert a minature files for easier test figure
# otherwise it just spent so many time to construct a graph everytime I need to tune
# some variable

myshpfile[:5].to_file('helper_files/TaiwanCounties_Mini.geojson', driver='GeoJSON')
myshpfile.iloc[:5,:6].to_csv('helper_files/TaiwanCounties_Mini.csv', index=False)

# then the normal size
myshpfile.to_file('helper_files/TaiwanCounties.geojson', driver='GeoJSON')
myshpfile.iloc[:,:6].to_csv('helper_files/TaiwanCounties.csv', index=False)

# the simplified polygons
simple_shp = myshpfile


for i in range(len(myshpfile)):
    simple_geo = myshpfile.geometry[i].simplify(0.001, preserve_topology=False)
    simple_shp.geometry[i] = simple_geo

simple_shp.to_file('helper_files/TaiwanCounties_simple.geojson', driver='GeoJSON')
