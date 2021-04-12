# Getting the private key

## OpenSSL

Use OpenSSL one the certificate (`cacertificate.pem`) to get the modulus and the public exponent

```bash
>   openssl x509 -in cacertificate.pem -noout -modulus

Modulus=E649D57F6FF9CFF655CB79EE38380C8F8278EB374A90059B0FF06534829D337C753D0E59AFED6FA489F015CF33
```

```bash
>   openssl x509 -in cacertificate.pem -noout -text

...
                Exponent: 65537 (0x10001)
...
```

In decimal the modulus is equal to:
```
2112664634855999140031945945998785346946804826144846396410436155861557104011009549879696604291518474904522547
```

## Cado

Use Cado-NFS to find the prime factors of the modulus

``` bash
>   ./cado-nfs.py <modulus> -t 4

1524938362073628791222322453937223798227099080053904149 1385409854850246784644682622624349784560468558795524903
```

## Python

Use the Python script `gen_key.py` to generate a private key based on the public exponent and the prime factors

```bash
>   ./gen_key.py 1524938362073628791222322453937223798227099080053904149 1385409854850246784644682622624349784560468558795524903 65537

-----BEGIN RSA PRIVATE KEY-----
MIHkAgEAAi4A5knVf2/5z/ZVy3nuODgMj4J46zdKkAWbD/BlNIKdM3x1PQ5Zr+1v
pInwFc8zAgMBAAECLT/O74A7F53+5HDX3SDortpIzZZnIJrU93O2hwZom1NeFGiJ
kzyyMi8aQTGHiQIXD+vNKx7XRLvtGKRfICO2s5DWEwOGUxUCFw523+PB/OAFczNk
upoX1C9wkosNKEsnAhcLd9fesqVvXkqn0Gaw+Oi2qaJ6KbTNDQIXAZClKuyLYuXU
ECR++DtJzxQ8FuWGjZMCFwYnXyGcz8NzMENGa/lNLrkQ9D0gutHw
-----END RSA PRIVATE KEY-----
```

## Sign and verify

Now we can sign out better grade (`grade_better.txt`)

```bash
>   openssl dgst -md5 -sign cakey.pem -out grade_better.sign grade_better.txt
```

Get a public key from the certificate

```bash
>   openssl x509 -in cacertificate.pem -pubkey -noout

-----BEGIN PUBLIC KEY-----
MEkwDQYJKoZIhvcNAQEBBQADOAAwNQIuAOZJ1X9v+c/2Vct57jg4DI+CeOs3SpAF
mw/wZTSCnTN8dT0OWa/tb6SJ8BXPMwIDAQAB
-----END PUBLIC KEY-----
```

And verify the signature against that public key

```bash
>   openssl dgst -md5 -verify public_key.pem -signature grade_better.sign grade_better.txt

Verified OK
```
