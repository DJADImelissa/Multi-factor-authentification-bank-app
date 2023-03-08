from banque import app,db,mail
from flask import render_template, redirect, url_for,flash, get_flashed_messages
from banque.models import Question, User,Transaction
from banque.forms import RegisterForm ,LoginForm,QuestionForm,TransactionForm,VerifyForm
from flask_login import login_user,logout_user,login_required,current_user
from random import *
from flask_mail import Mail, Message
import sys
import os

#Construction de la table utilisée pour le cryptage et décryptage
def table_cesar():
    tab=[]
    for i in range(32,127):
        tab.append(chr(i))

    for i in range(161,256):
        tab.append(chr(i))
    return tab

#elle donne la position de la lettre dans la table prédéfinie table_cesar
def position(tab,x):
    return tab.index(x)

# """ 
#     Décale de n place(s) dans la table cesar 
# """    
def letterShift(letter, n, tab):
    return tab[(position(tab,letter) + n) % 190]

# """ 
#     Décale de n place(s) en arrière dans la table cesar  
# """ 
def letterShiftMoins(letter,n, tab):
    n = n % 190
    return tab[((position(tab,letter) - n) + 190)% 190] 
    

# """ 
#     Crypte un texte avec une clé saisie par l'utilisateur 
# """
def encryptTextKey(text):
    key = 5
    tab =table_cesar()
    encryptText = "" 
    
    for i in range(0, len(text)):
        character = text[i]
        
        if character != " ":
            encryptText = encryptText + letterShift(character, key, tab) 
        else:
            encryptText = encryptText + " "
    
    return encryptText 


# """ 
#    Décrypte le texte avec la clé saisie par l'utilisateur 
# """    
def decryptTextKey(text):
    key = 5 
    tab =table_cesar()
    decryptText = ''
    
    for i in range(0, len(text)):
        character = text[i]
        
        if character != " ":
            decryptText = decryptText + letterShiftMoins(character,key,tab)
        else:
            decryptText = decryptText + " "
    
    return decryptText
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

# @app.route('/trasn')
# @login_required
# def market_page():
#     items = Item.query.all()
#     return render_template('market.html', items=items)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    # form2=QuestionForm()
    print("hi ")
    if form.validate_on_submit():
        print("changement d'ambiance")
        numbers=randint(10000, 99999)
        user_to_create = User(username=encryptTextKey(form.username.data),
                              first_name=encryptTextKey(form.first_name.data),
                              last_name=encryptTextKey(form.last_name.data),
                              numero=encryptTextKey(str(form.numero.data)),
                              email_address=encryptTextKey(form.email_address.data),
                              password=form.password1.data,
                              code=encryptTextKey(str(numbers))
                    
                              )
        print(form.username.data)
        db.session.add(user_to_create)
        db.session.commit()

        user2=User.query.filter_by(username=encryptTextKey(form.username.data)).first()
        print(user2.id)
        # msg=Message('Code',
        #             sender ='testssad4@gmail.com',
        #             recipients = ['master.bigdataa.22@gmail.com']
        #             )
        # msg.body = user2.code
        # mail.send(msg)

        print("test44")
        question1_to_create = Question(question=encryptTextKey(form.question1.data),
                                      response=encryptTextKey(form.reponse1.data),
                                      user_id=user2.id
                                      )
        # print(question1_to_create)
        # modify the forms.py first 
        # question2_to_create = Question(question=form2.question2,
        #                             response=form2.reponse2.data,
        #                             user_id=user_to_create.id
        #                             )
        # question3_to_create = Question(question=form2.question3,
        #                             response=form2.reponse3.data,
        #                             user_id=user_to_create.id
        #                             )

        db.session.add(question1_to_create) 
        db.session.commit()
        # adding the other questions       
        # db.session.add(question2_to_create)        
        # db.session.add(question3_to_create)        
        
        
        #flask mail hna pour envoyer le code bancaire lel mail
        # user_to_create.code
        print('test')
        return redirect(url_for('home_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}',category='danger')

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data,code=form.code.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('dashboard_page'))
        else:
            flash('Username and password  and code are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route('/dashboard')
def dashboard_page():
    print("salut mev")
    print (current_user.id)
    transactions=Transaction.query.filter_by(user_id=current_user.id)
    for x in transactions:
        print (x.montant)
    return render_template('dashboard.html',transactions=transactions)

@app.route('/transactions', methods=['GET', 'POST'])
def transactions_page():
    form = TransactionForm()
    if form.validate_on_submit():
        # print (current_user.get_id())
        # print("5")
        # print(current_user.id)
        sender = User.query.get_or_404(current_user.id)
        print(sender)
        receiver = User.query.filter_by(username=form.receiver.data).first()
        montant=form.montant.data
        if sender  :
            if sender.owned_m >= montant :
                if montant < 1000000 :
                    transaction_to_create = Transaction(
                              montant=form.montant.data,
                              receiver=form.receiver.data,
                              user_id=current_user.id, 
                              )
                    db.session.add(transaction_to_create)
                    db.session.commit()
                    #modif bdd :
                    user_receiver=User.query.filter_by(username=form.receiver.data).first()
                    if user_receiver:
                        user_receiver.owned_m +=   montant
                        current_user.owned_m -=  montant
                    # sender.owned_m =  sender.owned_m - montant
                        db.session.commit()
                    flash(f'Successeful transaction', category='success')
                    return redirect(url_for('dashboard_page'))
                elif montant >= 1000000 and montant < 5000000 :
                    return redirect(url_for('verify_page'))
                else:
                    return redirect(url_for('error_page'))

    return render_template('transactions.html' , form=form)

@app.route('/verify', methods=['GET', 'POST'])
def verify_page():
    form=VerifyForm()
    question=Question.query.filter_by(user_id=1).first()
    print(current_user.id)
    print(question.question)
    if form.validate_on_submit():
        print("dkhlna")
        if(question.response!=form.reponse.data):
            return redirect(url_for('logout_page'))
        else:
            print("transaction effectu")

    return render_template('verify.html',form=form ,question=question)

@app.route('/error')
def error_page():
    render_template('erreur.html')