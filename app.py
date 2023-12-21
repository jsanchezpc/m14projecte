#-*-coding:utf-8-*-
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "m14-thos-project"

@app.route("/")
def home():
    session["hunger"] = 5
    session["thirst"] = 8

    session["p1_kitchen"] = ["/static/img/rooms/kitchen1.jpeg", "La clau no hi és, però uns bons macarrons si.", "/static/img/foody.svg"]
    session["p1_cola_room"] = ["/static/img/rooms/cola.jpeg", "Una habitació que si vinc sol estaria cagat... Es veritat, estic sol... Sol amb una cocacola!!", "/static/img/coke.svg"]
    session["p1_up"] = ["/static/img/rooms/up.jpeg", "Unes escales que porten al pis superior... Serà bona idea?"]
    session["p1_room1"] = ["/static/img/rooms/02.jpeg", "Aquesta habitació dona por... El que no dona es una clau secreta que podria servirme per alguna rao."]
    session["p1_room2"] = ["/static/img/rooms/04.jpeg", "He estat aqui abans?... No sé pero no tinc la clau"]
    session["p1_aspiradora"] = ["/static/img/rooms/aspi.jpeg", "Aqui podria estar la clau... Pero no la veig per ninguna part..."]

    session["p2_kitchen"] = ["/static/img/rooms/kitchen2.jpeg", "Un altre plat de macarrons?... Si surto d'aqui em compro un bittlet de loteria de navidad", "/static/img/foody.svg"]
    session["p2_down"] = ["/static/img/rooms/down.jpeg", "Per aqui es baixa al primer pis."]
    session["p2_cola_room"] = ["/static/img/rooms/cola.jpeg", "Ostres, tenia la boca com una sabata, i aqui veig una cocacola.", "/static/img/coke.svg"]
    session["p2_room1"] = ["/static/img/rooms/02.jpeg", "Epa! Una clau! Aixo em servirà!", "/static/img/key.svg"]
    session["p2_room2"] = ["/static/img/rooms/04.jpeg", "No veig res interessant per aqui... Tot es molt vell."]
    session["p2_room3"] = ["/static/img/rooms/05.jpeg", "Hauria 'utilitzar la clau aqui..."]

    session["map"] = [
        [session["p1_cola_room"], session["p1_room1"], session["p1_room2"]],
        [session["p1_aspiradora"], session["p1_up"], session["p1_kitchen"]],
        [session["p2_cola_room"], session["p2_down"], session["p2_kitchen"]],
        [session["p2_room2"], session["p2_room1"], session["p2_room3"]]
    ]
    session['posZ']=0
    session['posX']=1
    session["position"]=session["map"][int(session["posZ"])][int(session["posX"])]
    session['bg']=session["position"] 

    if len(session['bg']) > 2:
        return render_template('index.html', bg=session['bg'][0], thirst=session["thirst"], hunger=session["hunger"], info=session['bg'][1], item=session['bg'][2])
    else:
        return render_template('index.html', bg=session['bg'][0], thirst=session["thirst"], hunger=session["hunger"], info=session['bg'][1])
    
def get_new_position(current_posZ, current_posX, direction):
    if direction == "nord":
        return current_posZ + 1, current_posX
    elif direction == "sur":
        return current_posZ - 1, current_posX
    elif direction == "est":
        return current_posZ, current_posX + 1
    elif direction == "oest":
        return current_posZ, current_posX - 1
    else:
        return current_posZ, current_posX


@app.route("/do", methods=['POST'])
def move():
    if request.method == 'POST':
        user_input = request.form['action']

        # Extracting action from user input
        action, *direction = user_input.split()

        if action in ["anar", "agafar", "menjar", "beure"]:
            if action == "anar" and direction:
                specified_direction = direction[0]
                if specified_direction in ["nord", "sur", "est", "oest"]:
                    new_position_z, new_position_x = get_new_position(session['posZ'], session['posX'], specified_direction)
                    if 0 <= new_position_z < len(session['map']) and 0 <= new_position_x < len(session['map'][0]):
                        session['posZ'] = new_position_z
                        session['posX'] = new_position_x
                        session['position'] = session['map'][int(session['posZ'])][int(session['posX'])]
                        session['bg'] = session['position']
                        session["thirst"] -= 1
                        session["hunger"] -= 1
                        if len(session['bg']) > 2:
                            return render_template('index.html', bg=session['bg'][0], thirst=session["thirst"], hunger=session["hunger"], info=session['bg'][1], item=session['bg'][2])
                        else:
                            return render_template('index.html', bg=session['bg'][0], thirst=session["thirst"], hunger=session["hunger"], info=session['bg'][1])
                    else:
                        return redirect('/error')





@app.route('/gameover')
def gameover():
    return render_template('gameover.html')

@app.route('/error')
def error():
    return render_template('error.html')
    
@app.route('/reset')
def reset():
    print("Current game is ending.")
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)