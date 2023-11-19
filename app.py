# Importing required modules
from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_mail import *
from utility import *

# creating  flask application,
app = Flask(__name__)

# connecting with mysql database.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:PASSWORD@localhost/user'
app.config['SECRET_KEY'] = "e54a4a9fb8bd923330e643e31e0d7142"


# creating mail app.
mail = Mail(app)

# configuring the mail.
app.config['MAIL_SERVER']='smtp.gmail.com'  
app.config['MAIL_PORT']= 465  
app.config['MAIL_USERNAME'] = 'admin@gmail.com'  
app.config['MAIL_PASSWORD'] = 'password'
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True

#------------------------Code to create tables in database------------------
# Initializing mysql
db = SQLAlchemy(app)

# Creating table class for user table.
class Userrecord(db.Model):
     name = db.Column(db.String(80), nullable=False)
     username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
     email = db.Column(db.String(120), unique=True, nullable=False)
     password = db.Column(db.String(60), unique=True, nullable=False)

     def __init__(self, name, username, email, password):
            self.name = name
            self.username = username
            self.email = email
            self.password = password

class GameRecord(db.Model):
     id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement = True)
     user1 = db.Column(db.String(80), nullable=False, primary_key=False)
     user2 = db.Column(db.String(120), nullable=False)
     status = db.Column(db.String(30), nullable=False)

     def __init__(self, user1, user2, status):
          self.user1 = user1
          self.user2 = user2
          self.status = status


# creating all the tables
with app.app_context():
      db.create_all()

#--------------------------Table creation ends here---------------------

#--------------------------Routing of different pages-------------------
@app.route('/')
def main():  
      return render_template('home.html', active_tab="home")


@app.route('/home')  
def home():  
      return render_template('home.html', active_tab="home")


# Routing login webpages
@app.route('/login', methods=['GET', 'POST'])
def login():
      if request.method == 'POST':
           username = request.form['username']
           password = request.form['password']
           existence = Userrecord.query.filter_by(username = username, password=password).first()
           if existence:
                session['username'] = request.form['username']
                board = GameRecord.query.filter_by(user1 = session['username']).all()
                return redirect(url_for('play'))
           return '<h1 style= "text-align: center;">Please enter correct user details OR Signup first.</h1>'
      
      #Redirect to game if user is already logged in.
      if 'username' in session:
            return redirect(url_for('play'))
      return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST']) 
def signup():
      if request.method == 'POST':
            r = request.form
            data = Userrecord(r['name'], r['username'], r['email'], r['password'])
            existing_user = Userrecord.query.filter_by(username = r['username']).first()
            if existing_user:
                 return '<h1 style= "text-alignment: center;">User already exists</h1>'
            db.session.add(data)
            db.session.commit()
            return render_template('login.html')
      return render_template('signup.html')


@app.route('/logout')
def logout():
     session.pop('username')
     return render_template('home.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
      if request.method == 'POST':
            msg = Message(subject='COntact form', sender=request.form['email'],
                           recipients=['nj223948@gmail.com'])
            msg.body = request.form['problem']
            try:
                  mail.send(msg)
            except Exception as e:
                 return f"{str(e)}"
            return "<h1 style='text-alignment: center;'> Received your concern, we will contact you soon.</h1>"
      return render_template('contact.html')


# Routing for game pages.
@app.route('/play', methods=['POST', 'GET'])
def play():
      if request.method == 'POST':
            if 'username' in session:
                  existence = Userrecord.query.filter_by(username = session['username']).first()
                  board = GameRecord.query.filter_by(user1 = session['username']).all()
                  return render_template('game.html', name = existence.name
                                         , score = score_board(board))                
            return render_template('game.html', class_name='visibility', score = [8] * 8)
      user = Userrecord.query.filter_by(username = session['username']).first()
      board = GameRecord.query.filter_by(user1 = session['username']).all()
      return render_template('game.html', name = user.name, score=score_board(board))  

@app.route('/gamedata', methods=['POST'])
def gamedata():
      if request.method == 'POST':
            if 'username' in session:
                  data = request.get_json()
                  entry = GameRecord(session['username'], data['user2'], data['status'])
                  db.session.add(entry)
                  db.session.commit()
                  board = GameRecord.query.filter_by(user1 = session['username']).all()
                  return render_template('game.html', name = 'Name', score=score_board(board))
      return 'Data recieved successfully'   


#----------------------------Main application------------------

if __name__ == '__main__':  
   app.run(debug = True)
