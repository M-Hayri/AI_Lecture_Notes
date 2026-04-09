"""
Örnekte verilen bilgiler:

1. Eğer yağmur yağmadıyssa Harry Hagrid'i ziyaret etti
2. Harry Hagrid'i ya da Dumbledorue'u ziyaret etti ama ikisi birden etmedi
3. Harry Dumbledore'u ziyaret etti.
4. Öyleyse yağmur yağmuş demektir.
"""

from logic import *

# yağmur, hagrid ve dumbledore nesneleri tanımla
rain = Symbol("rain")
hagrid = Symbol("hagrid")
dumbledore = Symbol("dumbledore")

knowledge = And(
    Implication(Not(rain), hagrid),
    Or (hagrid, dumbledore),
    Not(And(hagrid,dumbledore)),
    dumbledore
)
print(model_check(knowledge, rain)) #True