# 2Faing Out Challenge WU

<p align="center"><img src="./Screenshots/chall.png"></p>

## Source code analysis

````javascript
app.post('/forgot-password', (req, res) => {
    const { email } = req.body;
    const user = users.find(u => u.email === email);

    if (!user) {
        return res.status(401).send("You must be logged in.");
    }

    const token = crypto.createHash('sha256')
        .update((Date.now() >> 3).toString() + SECRET_KEY)
        .digest('hex');

    user.resetToken = token;

    res.send(`Token generated! <a href="/reset">Click here to reset password</a>`);
});
````

````javascript
app.post('/reset', (req, res) => {
    const { username, newPassword, resetToken} = req.body;

    const currentUser = users.find(u => u.username === username && u.resetToken === resetToken);

    if (currentUser) {
        console.log(`Resetting ${currentUser.username} password`);
        currentUser.password = newPassword;
        currentUser.resetToken = null;
        return res.redirect('/dashboard');
    }

    res.status(403).send("Error updating password: No valid reset session found.");
});
````
````javascript
const users = [
    {
        username: 'admin',
        password: process.env.ADMIN_PASSWORD,
        email: 'admin@example.com',
        resetToken: null
    },
    {
        username: 'attacker',
        password: 'attacker',
        email: 'attacker@example.com',
        resetToken: null
    }
];
````

## Flag:

FLAG: _PWNED{_!_h4ve_7o1d_y0u_t0_u$e_2f@}_
