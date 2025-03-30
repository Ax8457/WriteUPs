# The Hearth of the Gearford Write-Up

<p align="justify">This challenge was a MISC one, in which the server machine must have been rooted to read the flag. To do so authentication mecanism source code was provided and is attached in this repo under cryptoAuth/... . The challenge was made of 3 parts: </p>

- Step 1 : Get an admin access (token signed with HMAC), attacking the authentication mecanism
- Step 2 : Get a RCE (and a webshell) on the admin panel using log poisoning method
- Step 3 : Get a revshell and perform a privesc to read the flag located in /root/flag.txt

<p align="center">
<img src="Screenshots/S1.png" style="width: 40%">
</p>

<h2> creenshot from 2025-03-30 22-02-57Step 1 : Time based attack on rust server </h2>
