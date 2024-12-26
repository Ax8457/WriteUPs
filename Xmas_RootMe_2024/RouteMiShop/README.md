# Route Mi Shop (day10)

<p align="justify">This challenge was a Web challenge in which a e-shop was deployed. We were asked to credit enough an account to be able to buy the flag. The source code was provided and is attached in this repo.</p>
<p align="center"><img src="Screenshots/S1.png" alt="Desc"></p>

<p align="center"><img src="Screenshots/S2.png" alt="Desc"></p>

````python
def anti_bruteforce(time):
    return sleep(time)
````
````python
@app.route('/discount', methods=['POST'])
@login_required
def discount():
    user = User.query.get(session['user_id'])
    coupon_code = request.form.get('coupon_code')

    coupon = Coupon.query.filter_by(user_id=user.id, code=coupon_code).first()

    balance = int(user.balance)
    if coupon:
        if not coupon.used:
            balance += 5.0
            user.balance = balance
            db.session.commit()

            anti_bruteforce(2)

            coupon.used = True
            user.can_use_coupon = False
            db.session.commit()
            flash("Your account has been credited with 5€ !")
        else:
            flash("This coupon has already been used.")
    else:
        flash("This coupon is invalid or does not belong to you.")

    return redirect(url_for('account'))
````

<p align="center"><img src="Screenshots/S4.png" alt="Desc"></p>

<p align="center"><img src="Screenshots/S3.png" alt="Desc"></p>

Flag : _RM {Route-m1_F0r_Th3_W1n}_ , thanks _Elweth_ for this challenge ! 


