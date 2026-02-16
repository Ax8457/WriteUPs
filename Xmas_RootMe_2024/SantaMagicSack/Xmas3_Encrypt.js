const CryptoJS = require("crypto-js");
const secretKey = "S4NT4_S3CR3T_K3Y_T0_ENCRYPT_DATA";
function encryptJSON(obj) {
    const jsonString = JSON.stringify(obj);
    const encrypted = CryptoJS.AES.encrypt(jsonString, secretKey).toString();
    return encrypted;
}

const data={
  playerName: 'axel',
  score: 133338,
  checksum: 'a94127642cf2ef8f5eb3896c57afa9df535038ae36ce0358dbcb7aea4650d08b',
  salt: 1
}

const encryptedData = encryptJSON(data);
console.log("[+] Cipher: ", encryptedData);
