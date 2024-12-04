# Challenge Santa's Magic Sack (day3)

<p align="center"><img src="Screenshots/S1.png" alt="Desc"></p>

In this challenge, a game written in javascript is deployed on a website. It consists in collected gifts falling by moving a santa sack laterally. The clock is limited to 20 seconds and the goal is to beat Santa's score which is 133337 points. Obviously it's impossible to beat this score within only 20 seconds and a way to cheat must be found to beat it. 

<p align="center"><img src="Screenshots/S4.png" alt="Desc" style="width:70%"></p>

The source code wasn't porvided directly but was available in the browser inspection section so the very first thing I did had been copy-pasting the code I got inspecting the browser to <a href="https://beautifier.io"> beautifier.io </a> to make the javascript code readable. The source code is provided under Xmas3_Src.js in this repo. I quickly identified the function which was in charge of sending score to server. It appeared that the score was sent through JSON to server :  

````javascript
async function Vd(e, t) {
    const {
        checksum: r,
        salt: n
    } = $d(e, t), l = Wd({
        playerName: e,
        score: t,
        checksum: r,
        salt: n
    });
    try {
        return await (await fetch("/api/scores", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                data: l
            })
        })).json()
    } catch (i) {
        return console.error("Error submitting score:", i), {
            success: !1
        }
    }
`````

Besides, the JSON seemed to be sent with a checksum (to ensure the integrity of the score) and ecrypted with AES algorithm as the code snippet below shows :

````javascript
function $d(e, t) {
    const r = Math.floor(Math.random() * 9) + 1,
        n = `${e}-${t}-${r}`;
    return {
        checksum: gf.SHA256(n).toString(),
        salt: r
    }
}
````

<p align="center"><img src="Screenshots/S2.png" alt="Desc"></p>

Flag : _RM{S4NT4_H0PE_Y0U_D1DN'T_CHEAT}_ , thanks again _Elweth_ for this challenge !
