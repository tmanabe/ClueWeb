# ClueWeb
Tools for the ClueWeb document collections.
## Usage of ClueWebServer.py
### ClueWeb09 example
`python ClueWebServer.py E: F:`

(On another terminal window)

`wget http://localhost:8080/clueweb09-en0000-11-22222`

### ClueWeb12 example (in case of 2x 4TB HDDs)

`python ClueWebServer.py --twelve E:/Disk01 E:/Disk02 F:/Disk03 F:/Disk04`

(On another terminal window)

`wget http://localhost:8080/clueweb12-0000wb-11-22222`
