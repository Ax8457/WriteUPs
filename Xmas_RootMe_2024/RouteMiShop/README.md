# Route Mi Shop (day10)

<p align="justify">This challenge was a Web challenge in which an e-shop was deployed. We were asked to credit enough an account to be able to buy the flag. The source code was provided and is attached to this repo.</p>

<p align="center"><img src="Screenshots/S1.png" alt="Desc"></p>

<p align="justify">The first thing I did was creating an account and looking for a way to credit my account. After a few read of the source code, it seemed like a coupon was generated for every new account and credit the account with 5$. Unfortunately coupons were submitted to veririfcation before being used to avoid re-use or impersonation. </p>

<p align="center"><img src="Screenshots/S2.png" alt="Desc"></p>

<p align="justify">Going on the reading of the source code I noticed a function designed to avoid coupon bruteforce, which was simply doing a sleep during coupon submission:</p>

````python
def anti_bruteforce(time):
    return sleep(time)
````

<p align="justify">Actually this function was used by discount function in the route below, designed to get the 5$ discount using the coupon generated and coupled with the account. The function was checking wether the account who submitted the coupon was the one coupled with it (using user_id) and wether this coupon hadn't been used yet. To check that a boolean was set to False after the discount had been applied for every coupon. </p>

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

<p align="justify">Actually, it was possible to re-use the coupon because the boolean was set after anti_bruteforce() call. Hence, the server was sleeping for 2 secondes and then applying the discount. To exploit this weakness in coupon management, I intercepted the post request to server and spammed the button to relay it to server. After that my account was credited with 75$ :</p>

<p align="center"><img src="Screenshots/S4.png" alt="Desc"></p>

Finaly, I bought the flag which costed only 50$ and got it :

<p align="center"><img src="Screenshots/S3.png" alt="Desc"></p>

Flag : _RM {Route-m1_F0r_Th3_W1n}_ , thanks _Elweth_ for this challenge ! 


