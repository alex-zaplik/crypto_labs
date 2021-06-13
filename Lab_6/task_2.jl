include("elgamal.jl")

println("Using E-382:\n\t", E382Model)

PubKey, PriKey = generate(E382Model)

println("PubKey = ", PubKey)
println("PriKey = ", PriKey)

for i in 1:10
    P = random_point(E382Model)

    println("Testing on:\n\t", P)

    C = encrypt(E382Model, PubKey, P)
    Q = decrypt(E382Model, PriKey, C)

    if P == Q
        println("Success!")
    else
        println("Values are different:")
        println("\t", P)
        println("\t", Q)
        println("The cyphertext was:")
        println("\t", C)
    end
end
