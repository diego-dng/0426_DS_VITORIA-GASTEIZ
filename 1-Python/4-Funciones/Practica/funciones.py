from math import pi

def dia_semana(numero):
    """
    FUNCION QUE PIDE UN NUMERO ENTRE 1 Y 7 Y TE 
    DA EL NUMERO DE LA SEMANA
    """

    try:
        numero = int(numero)
        print(type(numero))
        if numero == 1:
            dia = "Lunes"
        elif numero == 2:
            dia = "Martes"
        elif numero == 3:
            dia = "Miercoles"
        elif numero == 4:
            dia = "Jueves"
        elif numero == 5:
            dia = "Viernes"
        elif numero == 6:
            dia = "Sabado"
        elif numero == 7:
            dia = "Domingo"
        else:
            dia = "Numero fuera de rango"

        return dia
    except:
        return "Tiene que ser un numero"
    

def piramide(num):
    lista = list(range(num, 0, -1))
    for i in lista.copy():
        print(*lista)
        lista.remove(i)

def comp(num1, num2):
    print(num1)
    print(num2)
    if num1 == num2:
        return "Son iguales"
    elif num1 > num2:
        return "El primer numero es mayor que el segundo"
    else:
        return "El segundo numero es mayor que el primero" 

def cont_letras(texto, letra):
    texto = texto.lower()
    letra = letra.lower()
    return texto.count(letra)

def conteo(texto):
    dict = {}
    texto = texto.lower()

    for i in texto:
        if i == " ":
            continue
        dict[i] = texto.count(i)

    return dict

def modificar_lista(lista, comando, elemento = None):
    comando = comando.lower()
    if comando == "add":
        lista.append(elemento)
    elif comando == "remove":
        if elemento in lista:
            lista.remove(elemento)
        else:
            return "elemento no encontrado en la lista"
    else:
        return "comando incorrecto"
    
    return lista

def frase(*ar):
    print(type(ar))
    return " ".join(ar)

def fibonacci(n):
    if n >= 0:
        if n == 0 or n == 1:
            return n
        else:
            return fibonacci(n-1) + fibonacci(n-2)
    else:
        return "El numero es negativo"
    
def area_cuadrado(l):
    return l**2

def area_triangulo(b,a):
    return b*a / 2

def area_circulo(r):
    return pi *r **2