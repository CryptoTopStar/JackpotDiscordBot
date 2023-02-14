import flask
from flask_cors import CORS
import pickle
import os
import database

app = flask.Flask(__name__)
CORS(app)

def writeTask(task):
    if not os.path.exists('./Cache/task.txt'):
        open('./Cache/task.txt', 'w').close()
    
    ## add the task to the file
    with open('./Cache/task.txt', 'a') as f:
        f.write(task + '\n')

@app.route('/invited', methods=['GET'])
def invited():
    ## IN THIS FORMAT: FH82-0XI-RP2
    referalCode = pickle.load(open('./Cache/Backup/referalCode.pickle', 'rb'))
    code = flask.request.args.get('code', None)
    print(code, referalCode)
    if code in referalCode:
        serverID = referalCode[code][0]
        memberID = referalCode[code][1]
        writeTask("INVITE|n|" + str(serverID) + "|n|" + str(memberID))
        return flask.jsonify({"mes": "guild has been invited"})
    else:
        return flask.jsonify({"mes": "error: code invalid"})
    
@app.route('/jackpot', methods=['GET'])
def resetJackpot():
    amount = flask.request.args.get('amount', None)
    date = flask.request.args.get('date', None)
    winners = flask.request.args.get('winners', None)
    writeTask("JACKPOT|n|" + str(amount) + "|n|" + str(date) + "|n|" + str(winners))
    return flask.jsonify({"mes": "jackpot update has been added to the command queue, and will be processed shortly"})

@app.route('/servers', methods=['GET'])
def resetJackpot():
    servers = pickle.load(open('./Cache/Backup/SERVER_NAMES.pickle', 'rb'))
    return flask.jsonify(servers)

@app.route('/mission', methods=['GET'])
def missionReply():
    missionID = flask.request.args.get('id', None)
    feedback = flask.request.args.get('feedback', None)
    database.finish_mission(missionID)
    writeTask("MISSION|n|" + str(missionID) + "|n|" + str(feedback))
    return flask.jsonify({"mes": "quest received, and will be processed shortly"})
    
## start the flask app, port 5000
app.run(port=5000)