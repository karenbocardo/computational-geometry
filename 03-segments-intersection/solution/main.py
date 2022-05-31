from algoritmo import AlgoritmoBarrido
from Punto import Punto
from Segmento import Segmento

def main():
    '''
    s1 = Segmento(Punto(10,10), Punto(0,0))
    s2 = Segmento(Punto(10,0), Punto(0,10))

    segmentos = [s1,s2]

    for s in segmentos:
      print(s)
    '''
    def read_file(filename):
        file = open(filename)
        return file.read().splitlines()

    # data = read_file(sys.argv[1])
    data = read_file('0.in')
    if len(data[0].split()) < 2: data.remove(data[0])
    segments = list()
    for line in data:
        sep = line.split()
        point1 = Punto(float(sep[0]), float(sep[1]))
        point2 = Punto(float(sep[2]), float(sep[3]))
        if len(sep) > 4:
            name = sep[4]
            segment = Segmento(point1, point2)
        else:
            segment = Segmento(point1, point2)
        segments.append(segment)

    barr = AlgoritmoBarrido(segments)
    barr.barrer()
    print(barr.R)

if __name__=="__main__":
    main()



