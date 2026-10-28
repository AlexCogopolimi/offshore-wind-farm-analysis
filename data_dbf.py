from dbfread import DBF
table = DBF("Grid_nazionale_20240221.dbf")
for x in table:
    if x['onshore']==0:
        if x['lat']>37.491461 and x['lat']<37.597634 and x['long']>15.584534 and x['long']<15.670179:
            print(x['lat'],'lat',x['long'],'long')
            print(x['dens_150'])
            print(x['vento_150'])
            print()
     
