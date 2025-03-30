# The Hearth of the Gearford Write-Up

<p align="justify">This challenge was a MISC one, in which the server machine must have been rooted to read the flag. To do so authentication mecanism source code was provided and is attached in this repo under cryptoAuth/... . The challenge was made of 3 parts: </p>

- Step 1 : Get an admin access (token signed with HMAC), attacking the authentication mecanism
- Step 2 : Get a RCE (and a webshell) on the admin panel using log poisoning method
- Step 3 : Get a revshell and perform a privesc to read the flag located in /root/flag.txt

<p align="center">
<img src="Screenshots/S1.png" style="width: 40%">
</p>

<h2> Step 1 : Time based attack on rust server </h2>


<p align="justify">Once on the page of the challenge, a message was redirecting on the /auth route so that the client could have received his token authentication. By default all clients were authenticated as Guest as shown in the snippet below : </p>

<p align="center">
<img src="Screenshots/S2.png" style="width: 40%">
</p>

<p align="justify">Actually, those tokens were signed with HMAC authentication algorithm. As show in the snipper below, token was composed of two parts; the first one which is the plaintext payload containing username and role, and the second </p>

````rust
pub fn receive_token(key: &[u8], plaintext_token: &[u8], authentication_tag: &[u8]) -> bool {
    let mut mac = Hmac::<Sha256>::new(key.into()); //format conversion
    mac.update(plaintext_token);
    let computed_tag = mac.finalize().into_bytes();
    verify(&computed_tag, authentication_tag)  
}
````

````rust
pub fn verify(expected: &[u8], received: &[u8]) -> bool {
    if expected.len() != received.len() {
        return false;
    }
    for (a, b) in expected.iter().zip(received.iter()) {
        if a != b {
            return false;
        }
        println!("Byte is valid.");
        thread::sleep(time::Duration::from_millis(10)); //longer check to make bruteforce attacks harder
    }
    true
}
````
