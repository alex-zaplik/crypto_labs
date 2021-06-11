# Merkle puzzles

## Example use of the script

```
> python merkle.py 24 24 
Parameters:
        Puzzle key size:        24 bits 
        Number of puzzles:      16777216

Alice:  Preparing puzzles
Alice:  Prepared 16777216 puzzles
Alice:  Shuffling puzzles

Bob:    Received 16777216 puzzles    
Bob:    Picking a random puzzle      
Bob:    Brute forcing a random puzzle
Bob:    Found a solution: key=10979469 message=b'A message prefix' 9142412 16974913111707538677490295290613439825865674948388180335009285274783899928930

Alice:  Received a puzzle id: 9142412

Alice:  Communication key: 16974913111707538677490295290613439825865674948388180335009285274783899928930
Bob:    Communication key: 16974913111707538677490295290613439825865674948388180335009285274783899928930

Alice:  Sending:        b'Hello Bob!\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16'
                        b"'\xbe\xd3\x97\xb6a\x82\x12E\x98\x9dh\x94\x1f,\xc1\x1a \xe4\xbb\xf0\x12\x85\x1a\x96x9\x92~k{`\xeaE\x08u\xeb\xbex\xa8\xa1\xc4\xccY\xe1\xd5\x88i"
Bob:    Received:       b"'\xbe\xd3\x97\xb6a\x82\x12E\x98\x9dh\x94\x1f,\xc1\x1a \xe4\xbb\xf0\x12\x85\x1a\x96x9\x92~k{`\xeaE\x08u\xeb\xbex\xa8\xa1\xc4\xccY\xe1\xd5\x88i"
                        b'Hello Bob!\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16'

Bob:    Sending:        b'Hello Alice!\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14'
                        b'\x9f\xc3\xa1\xb0\xe2t\xd3a\x82N\x0c\xac=I\xe5\xc4\x14\xc25\xc90\xd6\xb3y?\xec\x0e\x0b\x8fZ.\xdfp\x9f\x07*\xc0z\xaf"=\x8d\xeb\x7f\xa74\xbb8'
Alice:  Received:       b'\x9f\xc3\xa1\xb0\xe2t\xd3a\x82N\x0c\xac=I\xe5\xc4\x14\xc25\xc90\xd6\xb3y?\xec\x0e\x0b\x8fZ.\xdfp\x9f\x07*\xc0z\xaf"=\x8d\xeb\x7f\xa74\xbb8'
                        b'Hello Alice!\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14'

Puzzle memory usage:
        Message storage:        1342177280 bytes
        Key storage:            536870912 bytes

Timing:
        Puzzle generation:      580.47 seconds
        Puzzle cracking:        130.31 seconds
```
