const express = require('express');
const { Sequelize, DataTypes } = require('sequelize');
const ejs = require('ejs');

const app = express();
const flag = "FLAG{DOJO_54_TEST_FLAG}";

// sqlite
const sequelize = new Sequelize('sqlite::memory:', { logging: false });
const Users = sequelize.define('User', {
  session: DataTypes.STRING,
});

// pasrse cookie
function parseCookie(raw) {
  const sep = raw.indexOf(':');
  const id = Number(raw.slice(0, sep));
  const session = raw.slice(sep + 1);

  const bytes = Buffer.from(session, 'utf8');
  for (let i = 0; i < session.length; i++) {
    const b = bytes[i];
    const isLetter = (b >= 0x41 && b <= 0x5a) || (b >= 0x61 && b <= 0x7a) || b >= 0x80;
    if (!isLetter) throw new Error('invalid game session');
  }

  return JSON.parse(`{"id":${id}, "session":{"session":"${session}"}}`);
}

// html templ
const templateSource = `
<!DOCTYPE html>
<html>
<body>
  <h1>Output : <%= flag ? flag : "No flag (Invalid session)" %></h1>
</body>
</html>
`;
const indexTemplate = ejs.compile(templateSource);

// main
app.get('/', async (req, res) => {
  try {
    let output = "";
    const rawInput = req.query.cookie || "123:abcXYZ";
    const cookie = parseCookie(decodeURIComponent(rawInput));
    console.log("[+]cookie parsed:");
    console.log(cookie);
    console.log("[+]session parsed:");
    console.log(cookie["session"]);
    const record = await Users.findOne({
      where: cookie["session"],
    });
    const data = record?.dataValues || null;

    if (data !== null && data?.session === flag) {
      output = flag;
    }

    res.send(indexTemplate({ flag: output }));
  } catch (e) {
    res.status(400).send(`<b>Error :</b> ${e.message}`);
  }
});

// server
async function initServer() {
  await sequelize.sync({ force: true });
  //inject flag in db
  await Users.create({ session: flag });
  // std user
  await Users.create({ session: "abcXYZ" });

  app.listen(3000, () => {
    console.log(" Server on http://localhost:3000");
  });
}

initServer();
