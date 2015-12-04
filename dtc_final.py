# -----------------> importamos las librerias necesarias
from math import cos,sin,pi
from scipy.fftpack import dct,idct
import numpy as np
import random
from PIL import Image, ImageDraw,ImageFont
import os

#aqui esta la matriz de cuantificacion, la cual se usa en 
Q= [(16,11,10,16,24,40,51,61),
    (12,12,14,19,26,58,60,55),
    (14,13,16,24,40,57,69,56),
    (14,17,22,29,51,87,80,62),
    (18,22,37,56,68,109,103,77),
    (24,35,55,64,81,104,113,92),
    (49,64,78,87,103,121,120,101),
    (72,92,95,98,112,100,103,99)
]

qa = np.zeros((8,8))#declaramos una matriz de 8 x 8
for i in range(8):#recorremos el arreglo creado
    for j in range(8):
        qa[i][j] = Q[i][j]
# ------------------> tamano de la imagen
def vertam(imagen):
    stam = os.stat(imagen)
    return stam.st_size
# -----------------> aqui se carga la imagen
def cargar(imagen):
    im = Image.open(imagen)
    ancho, altura = im.size
    pixels = im.load()
    return ancho,altura,pixels,im   
# -----------------> creacion de la matriz temporal
def temmat(matriz):
    a = np.zeros((8,8))
    for i in range(8):
        for j in range(8):
            a[i][j] = matriz[i][j] - 128.0
    return a

# -----------------> aqui se aplica el dtc
def trans(a):
    global qa
    b = dct(a,type=2,n=None,axis=-1,norm='ortho',overwrite_x=False)
    c = idct(b, type=2, n=None, axis=-1, norm='ortho', overwrite_x=False)
    F = np.zeros((8,8))
    for i in range(8):
        for j in range(8):
            F[i][j] = b[i][j]/qa[i][j]
    return F

# -----------------> proceso
def regr(mat):
    global qa
    new = np.zeros((8,8))
    for i in range(8):
        for j in range(8):
            new[i][j] = mat[i][j]*qa[i][j]
    c = idct(new, type=2, n=None, axis=-1, norm='ortho', overwrite_x=False)

    for i in range(8):
        for j in range(8):
            c[i][j] = c[i][j] + 128
    return c
    
def proces(imagen):
    escala(imagen) ##transformamos imagen a escalas de grises
    ancho,altura,pixels,im = cargar("gris.jpg") ##cargamos imagen a gris
    i = 0
    j = 0
    arreglo = []
    i = 0
    j = 0
    while i < altura: ##recorre la imagen
        while j < ancho:
            if ancho - j >= 8 and altura - i >= 8:
                mat = []
                for k in range(8): ##bloques de ocho
                    mat.append([])
                    for l in range(8): 
                        #ash += 1
                        mat[k].append(pixels[l+j,k+i][0]) ##vamos guardando la matriz
                mat = temmat(mat) ##pasamos la matriz en formato de numpy
                mat = trans(mat) ##hacemos la transformada y la cuantificacion
                conts = 0
                for k in range(8):
                    for l in range(8):
                        if mat[k][l] != 0 and abs(mat[k][l]) < 1: #modificamos
                            mat[k][l]  = 0.0                      #3la matriz cuantificada
                            conts += 1 
                finaly = regr(mat) ##aplicamos inverso de dct
                for k in range(8): ##pintamos nuevamente
                    for l in range(8):
                        pixels[j+l,i+k] = (int(finaly[k][l]),int(finaly[k][l]),int(finaly[k][l]))
                j = j + 8
            else:
                j = j + 1
        i = i + 8
        j = 0
    im.save("finall.jpeg")
    return
#######################proceso#############################################################    
def escala(imagen):
    ancho,altura,pixels,im = cargar(imagen)
    for i in range(ancho):
        for j in range(altura):
            (a,b,c) = pixels[i,j]
            suma = a+b+c
            prom = int(suma/3)
            a = prom ##igualamos                                                                                                              
            b = prom ##igualamos                                                                                                              
            c = prom ##igualamos                                                                                                              
            pixels[i,j] = (a,b,c) ##igualamos                                                                                                 
    im.save("gris.jpg") ##guardamos la imagen nueva                                                              
    return
#aqui esta el metodo principal, el cual se ejecuta cuando inicia el programa y llama a los diferentes metodos creados
def main():
    print "Bienvenido, este programa calculara la dtc, partiendo de una imagen"
    print "Elaborado por equipo 3, del grupo 7 B\n"
    imagen = raw_input("Ingresa la ruta donde se encuentra la imagen : --> ")
    proces(imagen)
    uno = vertam("gris.jpg")
    dos = vertam("finall.jpeg")
    print "Peso de la imagen original : ",uno," bytes vs peso de la imagen comprimida : ",dos," bytes"
    print "El porcentaje total de compresion aplicando el algoritmo es de --> ",100.0 - (float(dos)*100.0)/float(uno)," %"
main()