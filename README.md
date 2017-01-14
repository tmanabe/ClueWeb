# ClueWeb
Tools for the ClueWeb document collections.
## Usage of ClueWebServer.py
### ClueWeb09 example
`python ClueWebServer.py E: F:`

(On another terminal window)

`wget http://localhost:8080/clueweb09-en0000-11-22222`

### ClueWeb12 example (in case of 2x 4TB HDDs)

`python ClueWebServer.py --twelve E:/Disk1 E:/Disk2 F:/Disk3 F:/Disk4`

(On another terminal window)

`wget http://localhost:8080/clueweb12-0000wb-11-22222`
