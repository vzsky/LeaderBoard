from flask import Flask, render_template
from flask_socketio import SocketIO
import collections

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

number = 5

schools = ['โรงเรียนเพลินพัฒนา', 'โรงเรียนกำเนิดวิทย์', 'โรงเรียนสามเสนวิทยาลัย', 'โรงเรียนมหิดลวิทยานุสรณ์', 'โรงเรียนระยองวิทยาคม']
score = [0] * number

@app.route('/update')
def sessions():
    return render_template('session.html', schools=zip(range(number), schools))

@app.route('/')
def index():
    return render_template('index.html', number=number)


def cal_score(data) :
    global score
    try :
        score[int(data['school'])] += int(data['amount'])
    except Exception as e :
        print(e)
    dat = dict(zip(schools, score))
    dat = [(k, dat[k]) for k in sorted(dat, key=dat.get, reverse=True)]
    return dat

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on("request")
def leaderboard():
    print("leaderboard connected")
    board = dict(zip(schools, score))
    board = [(k, board[k]) for k in sorted(board, key=board.get, reverse=True)]
    socketio.emit('my response', board, callback=messageReceived)

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', cal_score(json), callback=messageReceived)


if __name__ == '__main__':
    socketio.run(app, debug=True)
