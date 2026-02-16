const CryptoJS = require("crypto-js");
const secretKey = "S4NT4_S3CR3T_K3Y_T0_ENCRYPT_DATA";
function decryptData(encryptedData) {
    const bytes = CryptoJS.AES.decrypt(encryptedData, secretKey);
    const decryptedData = bytes.toString(CryptoJS.enc.Utf8);
    return JSON.parse(decryptedData);
}

const encryptedData = "U2FsdGVkX19qd5093wUagRzVbx5eX/7Jrv7Zm+KCk3XRsozT0ELlG1q7gzmQE8maENCorZe9ed/6tOjy44MZYFBBfu/8tL7qohFj+So1qAMEmY6vVPKVMi9IF50raqd7Ip6V+d1jgNJ6WVynbU02Hc8S25QzRkRVEXIKtWpFYS1l2tx5gsq9WK/4iL+xfk/S";
const decryptedData = decryptData(encryptedData);

console.log("[+] Plaintext :", decryptedData);
