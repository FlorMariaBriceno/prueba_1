def gauss_to_orca():
    entrada = input("Introduce un string de números atómicos: ")

    # Reemplazar guiones por dos puntos
    resultado = entrada.replace('-', ':')

    # Reemplazar comas por espacios
    resultado = resultado.replace(',', ' ')

    # Dividir el string en elementos y restar 1 a cada número
    elementos = resultado.split(' ')
    resultado = []
    for elemento in elementos:
        if ':' in elemento:
            inicio, fin = map(int, elemento.split(':'))
            resultado.append(f"{inicio - 1}:{fin - 1}")
        else:
            resultado.append(f"{int(elemento) - 1}")

    # Unir los resultados en un nuevo string
    resultado = ' '.join(resultado)

    # Mostrar el resultado
    print("Resultado final de la conversión de formato Gaussian a ORCA:")
    print(resultado)


def orca_to_gauss():
    entrada = input("Introduce un string de números atómicos: ")

    # Reemplazar dos puntos por guiones
    resultado = entrada.replace(':', '-')

    # Reemplazar espacios por comas
    resultado = resultado.replace(' ', ',')

    # Dividir el string en elementos y sumar 1 a cada número
    elementos = resultado.split(',')
    resultado = []
    for elemento in elementos:
        if '-' in elemento:
            inicio, fin = map(int, elemento.split('-'))
            resultado.append(f"{inicio + 1}-{fin + 1}")
        else:
            resultado.append(f"{int(elemento) + 1}")

    # Unir los resultados en un nuevo string
    resultado = ','.join(resultado)

    # Mostrar el resultado
    print("Resultado final de la conversión de formato ORCA a Gaussian:")
    print(resultado)


def main():
    print("Este programa convierte una secuencia de átomos de formato Gaussian a ORCA y viceversa")
    print("para armar un input QM/MM o QM1:QM2")
    print("¿Qué quieres hacer?")
    print("    1) Convertir QMAtoms de ORCA a Layer de Gaussian")
    print("    2) Convertir Layer de Gaussian a QMAtoms de ORCA")

    what = input("Introduce un número (1 o 2): ")

    if what == '1':
        orca_to_gauss()
    elif what == '2':
        gauss_to_orca()
    else:
        print("Opción no válida. Por favor, introduce 1 o 2.")

if __name__ == "__main__":
    main()
