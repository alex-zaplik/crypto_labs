include("edwards.jl")

# Using E-382:
#   x^ + y^2 = 1 - 67254 * x^2 * y^2
#   modulus = 2^382 - 105
#   P = (3914921414754292646847594472454013487047137431784830634731377862923477302047857640522480241298429278603678181725699, 17)

E382Mod = BigInt(2)^382 - 105

E382Gen = Point(
    FieldElement(3914921414754292646847594472454013487047137431784830634731377862923477302047857640522480241298429278603678181725699, E382Mod),
    FieldElement(BigInt(17), E382Mod),
    FieldElement(E382Mod - 67254, E382Mod)
)
