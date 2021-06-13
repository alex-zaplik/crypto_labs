include("edwards.jl")

# Some basic values for testing
p = 1009
d = FieldElement(p - 11, p)
P = Point(FieldElement(7, p), FieldElement(415, p), d)
Q = Point(FieldElement(23, p), FieldElement(487, p), d)

println(P + Q)
println(Q + P)
