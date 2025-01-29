# Open The Door 
<p align="justify"> In this challenge the goal was to open port 14456 on the server machine, which was initially closed. To do so, disclose of /etc/knockd.conf was necessary to reveal the port knocking sequence and open the port for a few seconds. Hence the goal here was to perform an LFI attack, allowing load of knockd configuration files. </p>

<p align="justify">Looking at the website deployed, it appeared that it was possible to create/generate PDF based on 1 image file, and 1 text file. Actually injecting image field was useless insofar as an image was expected and push an other file type to PDF generation was triggering an internal server error. </p>

<p align="center">
<img src="Screenshots/S1.png">
</p>

<p align="justify">Trying to load /etc/passwd file led to a server error, which showed that the input was submitted to clearing function which was escaping specific chars : </p>

<p align="center">
<img src="Screenshots/S2.png">
</p>

<p align="justify">Nonetheless by doubling the dot and the slash it was possible to bypass filter. Actually it looked like filter was escaping the whole motif ../ at PDF generation, but not the . and the / separated. With the payload below it was possible to download a PDF containing knockd configuration file located at /etc/knockd.conf : </p>

````text
....//....//....//....//....//....//....//....//etc/knockd.conf
````

<p align="center">
<img src="Screenshots/S3.png">
</p>
