const CryptoJS = require("crypto-js");
const fetch = require('node-fetch');
const https = require('https');

//The KEY retrieved in plaintext in the source code
const Ud = "S4NT4_S3CR3T_K3Y_T0_ENCRYPT_DATA";

//functio to encrypt JSON payload using the KEY retreived
function encryptData(data) {
    const jsonString = JSON.stringify(data);  
    const encrypted = CryptoJS.AES.encrypt(jsonString, Ud).toString();
    return encrypted;
}

// The same function as you can find in the source code
function $d(e, t, salt) {
    const n = `${e}-${t}-${salt}`;
    return {
        checksum: CryptoJS.SHA256(n).toString(), 
        salt: salt
    };
}

async function main() {
    const playerName = 'axel';
    const score = 133338; // to beat Santa score 
    const salt = 1; // the salt retreived in the decrypted json 
    const { checksum } = $d(playerName, score, salt); //retreive chekcsum
    if (!checksum) {
        console.log("[x] Checksum not found.");
        return;
    }
    //payload to encrypt using KEY
    const data = {
        playerName: playerName,
        score: score,
        checksum: checksum,
        salt: salt
    };
    //encrypt payload and send data to server 
    const encryptedData = encryptData(data);
    let response = await sendDataToServer(encryptedData);  
    if (response.isNewRecord !== true) {
        console.log("[x] Attempt failed, trying again...");
        return;
    }
    console.log("[+] Game hacked !!! :", response);
}

async function sendDataToServer(encryptedData) {
    // Ignore SSL check 
    const agent = new https.Agent({ //custom Agent to ignore ssl check
        rejectUnauthorized: false // Disable SSL check
    });
    const response = await fetch('https://day3.challenges.xmas.root-me.org/api/scores', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            data: encryptedData
        }),
        agent: agent  // Use the custom agent with SSL check disabled
    });
    const result = await response.json();
    return result;
}

main();
