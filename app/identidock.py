from flask import Flask, Response, request
import requests
import hashlib
import redis


app = Flask(__name__)
cache = redis.StrictRedis(host='redis', port=6379, db=0)
salt = "UNIQUE_SALT"
default_name = 'Joe Bloggs 2'



@app.route('/monster/<name>')
def get_identicon(name):
    
    image = cache.get(name)

    if(image is None):
        print ('Chache miss', flush=True)
        r = requests.get('http://dnmonster:8080/monster/'+name + '?size=80')
        image = r.content

    return Response(image, mimetype='image/png')

@app.route('/', methods=['GET','POST'])
def mainpage():
   name = default_name

   if request.method == 'POST':
       name = request.form['name']
    
    
   salted_name = salt + name
   name_hash = hashlib.sha256(salted_name.encode()).hexdigest()

   header = '<html><head><title>IdentiDock </title></head><body>'
   body = '''<form method="POST">
            Hello <input type="text" name="name" value="{0}" />
            <input type="submit" value="submit" />
            </form>
            <p>You look like a:
            <img src="/monster/{1}" />

            <input type="hidden" value={2} />
            '''.format(name, name_hash, request.method)
   footer ="</body></html>"
   return header + body + footer

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')