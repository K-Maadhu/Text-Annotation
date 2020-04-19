from flask import *
from food_annotations import get_annotations

app = Flask('my-flask-app',template_folder=r'C:\Users\Administrator\AppData\Local\Programs\Python\Python36\Lib\site-packages\flask\template')
app.debug = True

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

@app.route("/")
def hello():
    return 'hello world'
	
@app.route("/hello")
def hello2():
	return 'hello'
	
@app.route("/hello/<name>")
def hello_name(name):
	return "Hello " + name

@app.route("/login/<name>")
def login_name(name):
	if name == 'admin':
		return (redirect(url_for('login_admin')))
	else:
		return (redirect(url_for('login_guest',user = name)))

@app.route("/admin")
def login_admin():
	return 'admin'

@app.route("/guest/<user>")
def login_guest(user):
	return 'hello guest' + user

	
@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/do')
def do():
   return render_template('response.html', inp_txt = 'Enter review text',output = " ")

@app.route('/proc',methods = ['POST', 'GET'])
def proc():
     
   if request.method == 'POST':
      print(request)
      revw = request.form['nm']
   else:
      revw = request.args.get('nm')
      
   if not(revw is None):
       value = Markup(get_annotations(revw))   
   else:
       value = ' '          
       
   return render_template('response.html', inp_txt = revw,output = value)