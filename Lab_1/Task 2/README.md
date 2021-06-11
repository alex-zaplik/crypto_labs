# MD5 Collisions

## Task

People at Gras realized their mistake and they changed the way RSA key
is generated.

Fortunately for you they did not change the way the sign SignService works (except the name
of the le)  they still use md5 for signing.

(May be helpful: only the rst three lines of the les are read).

## Generating a collision

Using a tool like HashClash we can perform a chosen prefix attack on the grade files:
```
>   cd hashclash/files
>   ls

grade.txt grade_better.txt

>   ../scripts/cpc.sh grade.txt grade_m.txt
```

The result of this are two files. One starts with the contents of `grade.txt`, the other with `grade_better.txt`. Both have suffixes that makes their MD5 the same:

```bash
>   md5sum grade_hash.txt

bb1c8ebe8b5d39eaaa648068d17992e0  grade_hash.txt

>   md5sum grade_better_hash.txt

bb1c8ebe8b5d39eaaa648068d17992e0  grade_better_hash.txt
```

The suffixes will not get detected because only the first three lines of the files are read.

## Attack

If the file with correct values gets signed:

```bash
>   openssl dgst -md5 -sign cakeySec.pem -out grade.sign grade_hash.txt
```

Then the file containing modified values will get accepted:

```bash
>   openssl dgst -md5 -verify public_key.pem -signature grade.sign grade_better_hash.txt

Verified OK
```
