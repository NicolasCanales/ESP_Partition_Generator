import getpass
import os

user = getpass.getuser()
tarjeta = 'esp32'
partitionPath = '\\AppData\\Local\\Arduino15\\packages\\esp32\\hardware\\esp32\\1.0.6\\tools\\partitions'
boardsPath = '\\AppData\\Local\\Arduino15\\packages\\esp32\\hardware\\esp32\\1.0.6\\'
nameCSV = 'defaultvibot2MB'
sizeTarjeta = 2


# Generacion del archivo de respaldo boards.txt
f = open ('C:\\Users\\'+ user+ boardsPath + 'boards.txt','r')
f2 = open ('C:\\Users\\'+ user+ boardsPath + 'boardsRESPALDO.txt','w')
for linea in f:
    f2.write(linea)

f.close()
f2.close()


# Verificacion de alguna configuracion pre establecida bajo el mismo nombre
f = open ('C:\\Users\\'+ user+ boardsPath + 'boards.txt','r')
f2 = open ('C:\\Users\\'+ user+ boardsPath + 'boardsAux.txt','w')
veri = 0
flagVeri = 0
for linea in f:
    if veri == 2:
        # f2.write('ANOTADO\n')
        f2.write(tarjeta + '.menu.PartitionScheme.'+ nameCSV +'=Vibot '+str(sizeTarjeta)+'MB spiffs(2MB APP/'+str(sizeTarjeta)+' MB TOTAL)'+ '\n')
        f2.write(tarjeta + '.menu.PartitionScheme.'+ nameCSV +'.build.partitions='+ nameCSV + '\n')

    if tarjeta + '.menu.PartitionScheme.'+ nameCSV in linea:
        veri = veri + 1
        flagVeri = 1
        print("ENCONTRADO")
    else:
        veri = 0
    
    
    if veri == 0:
        print(linea)
        f2.write(linea)
    
    
f.close()
f2.close()


# Caso donde no habia configuracion previa
if flagVeri != 1:
    f = open ('C:\\Users\\'+ user+ boardsPath + 'boards.txt','r')
    f2 = open ('C:\\Users\\'+ user + boardsPath + 'boardsAux.txt','w')

    for linea in f:
        print(linea)
        f2.write(linea)
        if tarjeta + '.menu.PartitionScheme.default.build.partitions' in linea:
            print("ENCONTRADO")
            f2.write(tarjeta + '.menu.PartitionScheme.'+ nameCSV +'=Vibot '+str(sizeTarjeta)+'MB spiffs(2MB APP/'+str(sizeTarjeta)+' MB TOTAL)'+ '\n')
            f2.write(tarjeta + '.menu.PartitionScheme.'+ nameCSV +'.build.partitions='+ nameCSV + '\n')
        
        
    f.close()
    f2.close()


# Se agregan las lineas restantes
f = open ('C:\\Users\\'+ user + boardsPath + 'boardsAux.txt','r')
f2 = open ('C:\\Users\\'+ user + boardsPath + 'boardsAux2.txt','w')

veri = 0
flagVeri = 0
for linea in f:
    if veri == 3:
        # f2.write('ANOTADO\n')
        f2.write(tarjeta + '.menu.FlashSize.'+ str(sizeTarjeta) +'M='+ str(sizeTarjeta) +'MB (128Mb)'+ '\n')
        f2.write(tarjeta + '.menu.FlashSize.'+ str(sizeTarjeta) +'M.build.flash_size='+ str(sizeTarjeta) +'MB'+ '\n')
        f2.write(tarjeta + '.menu.FlashSize.'+ str(sizeTarjeta) +'M.build.partitions='+ nameCSV + '\n')

    if 'esp32.menu.FlashSize.'+ str(sizeTarjeta) +'M' in linea:
        veri = veri + 1
        flagVeri = 1
        print("ENCONTRADO")
    else:
        veri = 0
    
    
    if veri == 0:
        print(linea)
        f2.write(linea)

f.close()
f2.close()

# Reorganizacion de archivos
os.remove('C:\\Users\\'+ user+ boardsPath+'boards.txt')
os.remove('C:\\Users\\'+ user+ boardsPath+'boardsAux.txt')
os.rename('C:\\Users\\'+ user+ boardsPath+'boardsAux2.txt', 'C:\\Users\\'+ user+ boardsPath+'boards.txt')