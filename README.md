# ClueWeb
Tools for the ClueWeb document collections.
## Usage of ClueWebServer.py
### ClueWeb09 example
`python ClueWebServer.py W: X:`

(On another terminal window)

`wget http://localhost:8080/clueweb09-en0000-11-22222`

### ClueWeb12 example (in case of 2x 4TB HDDs)

`python ClueWebServer.py --twelve Y:/Disk1 Y:/Disk2 Z:/Disk3 Z:/Disk4`

(On another terminal window)

`wget http://localhost:8080/clueweb12-0000wb-11-22222`


## Usage of ClueWeb{C,Dec}ompactor.py

### ClueWeb12 example (in case of 2x 4TB HDDs)

`cat ids | python ClueWebCompactor.py --twelve Y:/Disk1 Y:/Disk2 Z:/Disk3 Z:/Disk4 pickle`

`python ClueWebDecompactor.py pickle`

(On another terminal window)

`wget http://localhost:8080/clueweb12-0000wb-11-22222`
