# Custom HTTP Server (day8)

<p align="center"><img src="Screenshots/S1.png" alt="Desc" style="width:40%"></p>

````javascript
const cookie = {
        name: 'FLAG',
        value: 'RM{REDACTED}',
        domain: '127.0.0.1',
        path: '/',
        httpOnly: false,
        secure: false,
      };
````

````javascript
router.get('/api/redirect', (req, res) => {
  const { url } = req.query;
  if (url) {
    res.redirect(url);
  } else {
    res.badRequest();
  }
});
````

<p align="center"><img src="Screenshots/S2.png" alt="Desc"></p>
