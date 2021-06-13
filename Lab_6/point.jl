abstract type CurvePoint end

function iselliptic(x::Number, y::Number, d::Number)
    if typeof(x) <: FieldElement
        x^2 + y^2 == typeof(x)(1, x.p) + d * x^2 * y^2
    else
        x^2 + y^2 == 1 + d * x^2 * y^2
    end
end

function iselliptic(P::CurvePoint)
    iselliptic(P.x, P.y, P.d)
end

POINTTYPES = Union{Integer, PrimeField}

struct Point{T <: Number, S <: Number} <: CurvePoint
    x::T
    y::T
    d::S

    Point{T, S}(x, y, d) where {T <: Number, S <:Number} = new(x, y, d)
end

Point(x::Infinity, y::Infinity,d::T) where {T<:POINTTYPES} = Point{Infinity,T}(x, y, d)
Point(x::T, y::T, d::T) where {T<:POINTTYPES} = !iselliptic(x, y, d) ? throw(DomainError("Point is not on curve")) : Point{T,T}(x, y, d)
Point(x::Infinity, 𝑦::Infinity, d::T, p::T) where {T<:Integer} = Point(x, y, FieldElement(d, p))
Point(x::T, y::T, d::T, p::T) where {T<:Integer} = Point(FieldElement(x, p), FieldElement(y, p), FieldElement(d, p))

"Formats CurvePoint as (x, y) on x^2 + y^2 = 1 + d * x^2 * y^2 : Fp"
function show(io::IO, z::CurvePoint)
    if typeof(z.x) <: PrimeField
        x, y = z.x.n, z.y.n
    else
        x, y = z.x, z.y
    end

    if typeof(z.d) <: PrimeField
        d = z.d.n
        field = string(" : F", z.d.p)
    else
        a, b = z.a, z.b
        field = ""
    end

    # print(io, "(", x, ", ", y, ") on x^2 + y^2 = 1 + ", d, " * x^2 * b^2 ", field)
    print(io, "(", x, ", ", y, ")")
end

"""
Returns the point resulting from the intersection of the curve and the
straight line defined by the points P and Q
"""
function +(P::CurvePoint, Q::CurvePoint)
    T = typeof(P)
    S = typeof(P.d)

    if P.d != Q.d
        throw(DomainError("Points are not on the same curve"))
    end

    p = P.d.p
    d = P.d        

    x = (P.x * Q.y + P.y * Q.x) / (S(1, p) + d * P.x * P.y * Q.x * Q.y)
    y = (P.y * Q.y - P.x * Q.x) / (S(1, p) - d * P.x * P.y * Q.x * Q.y)

    return T(S(x), S(y), P.d)
end

"Scalar multiplication of a Point"
function *(c::Integer, P::Point)
    T = typeof(P)
    S = typeof(P.d)

    if c == 0
        return T(S(0), S(1), P.d)
    end

    if c == 1
        return P
    end

    Q = div(c, 2) * P
    Q = Q + Q

    if c % 2 == 1
        Q = P + Q
    end

    return Q
end

"Compares two points"
function ==(P::Point, Q::Point)
    return P.d == Q.d && P.x == Q.x && P.y == Q.y
end

"Reflects the point across the Y axis"
function reflect(P::Point)
    return Point(-P.x, P.y, P.d)
end

