include("edwards.jl")


struct ElGamal
    Gen::CurvePoint
    Mod::Number

    ElGamal(Gen, Mod) = new(Gen, Mod)
end


struct Cypher
    P::CurvePoint
    Q::CurvePoint

    Cypher(P, Q) = new(P, Q)
end


function random_point(Model::ElGamal)
    rand(BigInt(1):Model.Mod) * Model.Gen
end


function generate(Model::ElGamal)
    x = rand(BigInt(1):Model.Mod)
    PubKey = x * Model.Gen
    (PubKey, x)
end


function encrypt(Model::ElGamal, PubKey::CurvePoint, Msg::CurvePoint)
    r = rand(BigInt(1):Model.Mod)
    Cypher(r * Model.Gen, Msg + (r * PubKey))
end


function decrypt(Model::ElGamal, priKey::Number, Msg::Cypher)
    reflect(priKey * Msg.P) + Msg.Q
end
