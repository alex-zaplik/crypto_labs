abstract type PrimeField <: Number end

infield(x::Number,y::Number) = x >= 0 && x < y

"Represents FieldElement type in which n โ ๐นp and p โ โ"
struct FieldElement <: PrimeField
    n::Integer
    p::Integer
    FieldElement(n, p) = !infield(n, p) ? throw(DomainError("n is not in field range")) : new(n, p)
end

"Formats PrimeField as n : ๐นโ"
function show(io::IO, z::PrimeField)
    print(io, z.n, " : ๐น", z.p)
end

"Returns true if both n and p are the same"
==(a::PrimeField, b::PrimeField) = a.p == b.p && a.n == b.n
==(::PrimeField,::Integer) = false


"Adds two numbers of the same field"
function +(a::PrimeField, b::PrimeField)
    if a.p != b.p
        throw(DomainError("Cannot operate on two numbers in different Fields"))
    else
        n = mod(a.n + b.n, a.p)
        return typeof(a)(n, a.p)
    end
end

"Substracts two numbers of the same field"
function -(a::PrimeField, b::PrimeField)
    if a.p != b.p
        throw(DomainError("Cannot operate on two numbers in different Fields"))
    else
        n = mod(a.n - b.n, a.p)
        return typeof(a)(n, a.p)
    end
end

"Negates a number"
function -(a::PrimeField)
    n = mod(a.p - a.n, a.p)
    return typeof(a)(n, a.p)
end

"Multiplies two numbers of the same field"
function *(a::PrimeField, b::PrimeField)
    if a.p != b.p
        throw(DomainError("Cannot operate on two numbers in different Fields"))
    else
        n = mod(a.n * b.n, a.p)
        return typeof(a)(n, a.p)
    end
end

"Multiplies a PrimeField by an Integer"
function *(๐::Integer, x::PrimeField)
    n = mod(๐ * x.n, x.p)
    return typeof(x)(n, x.p)
end

"Returns xแต using Fermat's Little Theorem"
function ^(x::PrimeField, k::Int)
    n = powermod(x.n, mod(k, (x.p - 1)), x.p)
    return typeof(x)(n, x.p)
end

"Returns 1/x as a special case of exponentiation where k = -1"
function inv(x::PrimeField)
    n = powermod(x.n, mod(-1, (x.p - 1)), x.p)
    return typeof(x)(n, x.p)
end

function div(a::PrimeField, b::PrimeField)
    return a / b
end

"Returns a/b using Fermat's Little Theorem"
function /(a::PrimeField,b::PrimeField)
    if a.p != b.p
        throw(DomainError("Cannot operate on two numbers in different Fields"))
    else
        n = mod(a.n * powermod(b.n, a.p - 2, a.p), a.p)
        return typeof(a)(n, a.p)
    end
end
