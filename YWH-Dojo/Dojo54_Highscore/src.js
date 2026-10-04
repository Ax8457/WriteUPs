//https://dojo-yeswehack.com/challenge-of-the-month/dojo-54

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

async function main() {
  process.chdir('/tmp/app');
  await init()
  const indexTemplate = ejs.compile(
    fs.readFileSync('views/index.ejs', 'utf-8'),
    { filename: 'views/index.ejs' }
  );

  try {
    var output = ""
    const cookie = parseCookie(decodeURIComponent(""));

    const record = await Users.findOne({
      where: cookie["session"],
    });

    const data = record?.dataValues || null
    
    if (data !== null && data?.session == flag) {
      output = flag
    }



    console.log(indexTemplate({ flag: output }));
  } catch (e) {
    console.log(e);
  }
}

main()
