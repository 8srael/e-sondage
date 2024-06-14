import math

def simpson(f, a, b, n):
    h = (b - a) / n
    x = a
    result = f(a) + f(b)
    for i in range(1, n):
        x += h
        if i % 2 == 0:
            result += 2 * f(x)
        else:
            result += 4 * f(x)
    return result * h / 3

def simpson2(f, a, b, n):
    pas = (b - a) / n
    somme = (f(a) + f(b)) / 2 + 2 * f(a + pas / 2)  # On initialise la somme
    x = a + pas           # La somme commence à x_1 
    for i in range(1, n): # On calcule la somme 
        somme += f(x) + 2 * f(x + pas / 2)
        x += pas
    return somme * pas / 3   # On retourne cette somme fois le pas / 3  



if __name__ == "__main__":
    f = lambda x: math.sin(2.57*x +0.125) + 1.25
    a = 0
    b = 4
    for i in range(a, b):
        print(f(i))