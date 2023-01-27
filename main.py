from printer import printers
from flask import Flask, request
app = Flask(__name__)


"""
raw data
{
    "ip_camera": "192.168.10.10",
    "id": "AP123456"
}
"""

@app.route('/printCheck',  methods = ['POST'])
def printCheck():
   content = request.form.to_dict(flat=False)
   status  = printers[content['ip_camera'][0]].printCheck(content['id'][0])
   return f'status {status}'


app.run(host="127.0.0.1", port=5002)