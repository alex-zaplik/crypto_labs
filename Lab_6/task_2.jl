include("curves.jl")


function test_curve(C::Curve)
    model = C.Model
    println("Using ", C.Name, ":\n\t", model)

    PubKey, PriKey = generate(model)

    println("PubKey = ", PubKey)
    println("PriKey = ", PriKey)
    println()

    for i in 1:5
        P = random_point(model)

        println("Testing on:\n\t", P)

        C = encrypt(model, PubKey, P)
        Q = decrypt(model, PriKey, C)

        if P == Q
            println("Success!")
        else
            println("Values are different:")
            println("\t", P)
            println("\t", Q)
            println("The cyphertext was:")
            println("\t", C)
        end

        println()
    end
end


test_curve(E222)
println()
test_curve(E382)
println()
test_curve(E521)
