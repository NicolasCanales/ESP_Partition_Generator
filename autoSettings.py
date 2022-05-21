check = 0
base = 36
print("*******************************************************************")
print('* * * *           C O N F I G U R A C I O N             * * * * * *')
print('* * * *                      D E                        * * * * * *')
print('* * * *              P A R T I C I O N E S              * * * * * *')
print("*******************************************************************")
print('\n')
print("-> Introduzca el nombre de su configuración, ejemplo default16MB")
nameConfiguration = input()
print('. . . nombre guardado correctamente. (' +nameConfiguration+ ')')
print('\n')

while 1:
    print("-> Introduzca el tamaño de su memoria flash en MB:")
    sizeFlash = input()
    if int(sizeFlash) >= 2 and int(sizeFlash) <= 16:
        print('. . . valor ingresado valido')
        sizeFlash = 1024*1024*int(sizeFlash)
        break
    else:
        print('. . . valor NO VALIDO, intentelo nuevamente.')

print('\n')

print("-> Defina el tamaño NVS en KB (recomendado 20KB, probado para evitar errores):")
sizeNVS = input()
sizeNVS = int(sizeNVS) 
sizeNVS = sizeNVS*1024
resto = sizeFlash - sizeNVS
restoMB = (resto/1024)/1024
print( '. . . '+str(resto/1024) + " KB disponibles(" + str(restoMB)+" MB) en memoria.")
print('\n')


print("-> Defina el tamaño OTA Data en KB (recomendado 8KB, probado para evitar errores):")
sizeOTADATA = input()
sizeOTADATA = int(sizeOTADATA)
sizeOTADATA = sizeOTADATA*1024
resto = resto - sizeOTADATA
restoMB = (resto/1024)/1024
print( '. . . '+str(resto/1024) + " KB disponibles(" + str(restoMB)+" MB) en memoria.")
print('\n')


print("-> Defina el tamaño APP 0 en KB (escoger minimo 1024KB = 1MB):")
sizeAPP0 = input()
sizeAPP0 = int(sizeAPP0)
sizeAPP0 = sizeAPP0*1024
resto = resto - sizeAPP0 - (base*1024)
restoMB = (resto/1024)/1024
print( '. . . '+str(resto/1024) + " KB disponibles(" + str(restoMB)+" MB) en memoria.")
print('\n')

print("-> Requerirá uso de OTA? [S/N]")
answer = input()
while(check == 0):
    if(answer == "S"):
        print("-> Defina el tamaño APP 1 en KB:")
        sizeAPP1 = input()
        sizeAPP1 = int(sizeAPP1)
        sizeAPP1 = sizeAPP1*1024
        resto = resto - sizeAPP1 
        restoMB = (resto/1024)/1024
        print( '. . . '+str(resto/1024) + " KB disponibles(" + str(restoMB)+" MB) en memoria.")
        print('\n')

        check = 1
    elif(answer == "N"):
        print('-> Defina el tamaño SPIFFS en KB (maximo ' + str(resto/1024) +'KB):')
        sizeSPIFFS = input()
        sizeSPIFFS = int(sizeSPIFFS)
        sizeSPIFFS = sizeSPIFFS*1024
        resto = resto - sizeSPIFFS 
        restoMB = (resto/1024)/1024
        print( '. . . '+str(resto/1024) + " KB de sobra (" + str(restoMB)+" MB) en memoria.")
        print('\n')
        check = 2
    else:
        print( '. . . '+"Comando incorrecto, responda <S> o <N>")
        answer = input()

if(check == 1):
    print('-> Defina el tamaño SPIFFS en KB (maximo ' + str(resto/1024) +'KB):')
    sizeSPIFFS = input()
    sizeSPIFFS = int(sizeSPIFFS)
    sizeSPIFFS = sizeSPIFFS*1024
    resto = resto - sizeSPIFFS 
    restoMB = (resto/1024)/1024
    print( '. . . '+str(resto/1024) + " KB de sobra (" + str(restoMB)+" MB) en memoria.")
    print('\n')

offsetInit = 36864
offset1 = int(offsetInit) + int(sizeNVS)
offset2 = int(sizeOTADATA) + int(offset1)
offset3 = int(sizeAPP0) +int(offset2)
if(check ==1):
    offset4 = int(offset3) +int(sizeAPP1)

lineNVS = "nvs, data, nvs, "+ str(hex(offsetInit)) +", "+  str(hex(sizeNVS)) +",\n" 
lineOTADATA = "otadata,  data, ota,  "+  str(hex(offset1)) +", "+  str(hex(sizeOTADATA)) +",\n"
lineAPP0 = "app0, app,  ota_0,"+  str(hex(offset2)) +", "+  str(hex(sizeAPP0)) +",\n"
if(check ==1):
    lineAPP1 = "app1,     app,  ota_1, "+  str(hex(offset3)) +", "+  str(hex(sizeAPP1)) +",\n"
    lineSPIFFS = "spiffs,   data, spiffs,"+  str(hex(offset4))+", "+  str(hex(sizeSPIFFS)) +",\n"
else:
    lineSPIFFS = "spiffs,   data, spiffs,"+  str(hex(offset3)) +", "+ str( hex(sizeSPIFFS)) +","


sizeAPP0 = round((sizeAPP0/1024)/1024)
sizeSPIFFS = round((sizeSPIFFS/1024)/1024)
# Segunda Parte
import getpass
import os

user = getpass.getuser()
tarjeta = 'esp32'
partitionPath = '\\AppData\\Local\\Arduino15\\packages\\esp32\\hardware\\esp32\\1.0.6\\tools\\partitions'
boardsPath = '\\AppData\\Local\\Arduino15\\packages\\esp32\\hardware\\esp32\\1.0.6\\'
nameCSV = nameConfiguration
sizeTarjeta = int((sizeFlash/1024)/1024)

# Creacion del CSV
for i in range(5):
    print(".\n")

print("Creando archivo de configuracion CSV ...\n")
f = open ('C:\\Users\\'+ user+ partitionPath + '\\'+nameConfiguration + '.csv','w')
f.write('# Name,   Type, SubType, Offset,  Size, Flags\n')
f.write(lineNVS)
f.write(lineOTADATA)
f.write(lineAPP0)
if(check ==1):
    f.write(lineAPP1)
    f.write(lineSPIFFS)
else:
    f.write(lineSPIFFS)
f.close()

print("Archivo creado con exito, espere...\n")
print('\n')
print('Creando respaldo de boards.txt ...')
# Generacion del archivo de respaldo boards.txt
f = open ('C:\\Users\\'+ user+ boardsPath + 'boards.txt','r')
f2 = open ('C:\\Users\\'+ user+ boardsPath + 'RESPALDO_boards.txt','w')
countLine = 0
for linea in f:
    f2.write(linea)
    countLine = countLine + 1
    if countLine%2000 == 0:
        print(".\n")
f.close()
f2.close()
print('Respaldo creado con exito!')
print('\n')
print('Configurando archivo boards.txt ...')
# Verificacion de alguna configuracion pre establecida bajo el mismo nombre
f = open ('C:\\Users\\'+ user+ boardsPath + 'boards.txt','r')
f2 = open ('C:\\Users\\'+ user+ boardsPath + 'boardsAux.txt','w')
veri = 0
flagVeri = 0
countLine = 0
for linea in f:
    if veri == 2:
        # f2.write('ANOTADO\n')
        f2.write(tarjeta + '.menu.PartitionScheme.'+ nameCSV +'=Vibot '+str(sizeTarjeta)+'MB ('+str(sizeAPP0)+'MB APP/'+str(sizeSPIFFS)+'MB SPIFFS)'+ '\n')
        f2.write(tarjeta + '.menu.PartitionScheme.'+ nameCSV +'.build.partitions='+ nameCSV + '\n')
        

    if tarjeta + '.menu.PartitionScheme.'+ nameCSV in linea:
        veri = veri + 1
        flagVeri = 1
    else:
        veri = 0
    countLine = countLine + 1
    if countLine%2000 == 0:
        print(".\n")

    if veri == 0:
        f2.write(linea)
    
if flagVeri == 1:
    print('Perfil creado con exito!')
    print('Nombre perfil de particiones: '+ 'Vibot ' +str(sizeTarjeta)+'MB ('+str(sizeAPP0)+'MB APP/'+str(sizeSPIFFS)+' MB SPIFFS)')
f.close()
f2.close()



# Caso donde no habia configuracion previa
if flagVeri != 1:
    countLine = 0
    f = open ('C:\\Users\\'+ user+ boardsPath + 'boards.txt','r')
    f2 = open ('C:\\Users\\'+ user + boardsPath + 'boardsAux.txt','w')

    for linea in f:
        countLine = countLine + 1
        if countLine%2000 == 0:
            print(".\n")
        # print(linea)
        f2.write(linea)
        if tarjeta + '.menu.PartitionScheme.default.build.partitions' in linea:
            # print("ENCONTRADO")
            f2.write(tarjeta + '.menu.PartitionScheme.'+ nameCSV +'=Vibot '+str(sizeTarjeta)+'MB ('+str(sizeAPP0)+'MB APP/'+str(sizeSPIFFS)+'MB SPIFFS)'+ '\n')
            f2.write(tarjeta + '.menu.PartitionScheme.'+ nameCSV +'.build.partitions='+ nameCSV + '\n')
    
    print('Perfil creado con exito!')        
    print('Nombre del perfil de particiones: '+ 'Vibot ' +str(sizeTarjeta)+'MB ('+str(sizeAPP0)+'MB APP/'+str(sizeSPIFFS)+' MB SPIFFS)')
    f.close()
    f2.close()


# Se agregan las lineas restantes
f = open ('C:\\Users\\'+ user + boardsPath + 'boardsAux.txt','r')
f2 = open ('C:\\Users\\'+ user + boardsPath + 'boardsAux2.txt','w')

veri = 0
flagVeri = 0
countLine = 0
for linea in f:
    if veri == 3:
        # f2.write('ANOTADO\n')
        f2.write(tarjeta + '.menu.FlashSize.'+ str(sizeTarjeta) +'M='+ str(sizeTarjeta) +'MB ('+str(sizeTarjeta*8)+'Mb)'+ '\n')
        f2.write(tarjeta + '.menu.FlashSize.'+ str(sizeTarjeta) +'M.build.flash_size='+ str(sizeTarjeta) +'MB'+ '\n')
        f2.write(tarjeta + '.menu.FlashSize.'+ str(sizeTarjeta) +'M.build.partitions='+ nameCSV + '\n')

    countLine = countLine + 1
    if countLine%2000 == 0:
        print(".\n")

    if 'esp32.menu.FlashSize.'+ str(sizeTarjeta) +'M' in linea:
        veri = veri + 1
        flagVeri = 1
    else:
        veri = 0
    
    
    if veri == 0:
        f2.write(linea)

f.close()
f2.close()

# Reorganizacion de archivos
os.remove('C:\\Users\\'+ user+ boardsPath+'boards.txt')
os.remove('C:\\Users\\'+ user+ boardsPath+'boardsAux.txt')
os.rename('C:\\Users\\'+ user+ boardsPath+'boardsAux2.txt', 'C:\\Users\\'+ user+ boardsPath+'boards.txt')

print('Proceso finalizado con exito!')
print('Reinicie el IDE de Arduino cerrando todas las ventanas previamente.')
