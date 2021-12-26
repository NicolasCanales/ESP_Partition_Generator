check = 0
print("**********************************************************")
print("Introduzca el nombre de su configuración:")
nameConfiguration = input()
print("nombre guardado correctamente.")
print(" ")

print("Introduzca el tamaño de su memoria flash en MB:")
sizeFlash = input()
sizeFlash = 1024*1024*int(sizeFlash) 
print(" ")

print("Tamaño NVS en KB:")
sizeNVS = input()
sizeNVS = int(sizeNVS) 
sizeNVS = sizeNVS*1024
resto = sizeFlash - sizeNVS
restoMB = (resto/1024)/1024
print( str(resto) + " bytes disponibles(" + str(restoMB)+" MB) en memoria.")
print(" ")


print("Tamaño OTA Data en KB:")
sizeOTADATA = input()
sizeOTADATA = int(sizeOTADATA)
sizeOTADATA = sizeOTADATA*1024
resto = resto - sizeOTADATA
restoMB = (resto/1024)/1024
print( str(resto) + " bytes disponibles(" + str(restoMB)+" MB) en memoria.")
print(" ")


print("Tamaño APP 0 en KB:")
sizeAPP0 = input()
sizeAPP0 = int(sizeAPP0)
sizeAPP0 = sizeAPP0*1024
resto = resto - sizeAPP0
restoMB = (resto/1024)/1024
print( str(resto) + " bytes disponibles(" + str(restoMB)+" MB) en memoria.")
print(" ")

print("Requerirá uso de OTA? [S/N]")
answer = input()
while(check == 0):
    if(answer == "S"):
        print("Tamaño APP 1 en KB:")
        sizeAPP1 = input()
        sizeAPP1 = int(sizeAPP1)
        sizeAPP1 = sizeAPP1*1024
        resto = resto - sizeAPP1
        restoMB = (resto/1024)/1024
        print( str(resto) + " bytes disponibles(" + str(restoMB)+" MB) en memoria.")
        print(" ")

        check = 1
    elif(answer == "N"):
        print("Tamaño SPIFFS en KB:")
        sizeSPIFFS = input()
        sizeSPIFFS = int(sizeSPIFFS)
        sizeSPIFFS = sizeSPIFFS*1024
        resto = resto - sizeSPIFFS
        restoMB = (resto/1024)/1024
        print( str(resto) + " bytes de sobra (" + str(restoMB)+" MB) en memoria.")
        print(" ")
        check = 2
    else:
        print("Comando incorrecto, responda <S> o <N>")
        answer = input()

if(check == 1):
    print("Tamaño SPIFFS en KB:")
    sizeSPIFFS = input()
    sizeSPIFFS = int(sizeSPIFFS)
    sizeSPIFFS = sizeSPIFFS*1024
    resto = resto - sizeSPIFFS
    restoMB = (resto/1024)/1024
    print( str(resto) + " bytes de sobra (" + str(restoMB)+" MB) en memoria.")
    print(" ")

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

print("*\n")
print("*\n")
print("*\n")
print("*\n")
print("*\n")
print("Creando archivo...\n")
f = open (nameConfiguration + '.csv','w')
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

print("Archivo creado con exito, revisar en carpeta compilada.\n")