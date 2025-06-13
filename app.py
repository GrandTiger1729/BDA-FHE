from flask import Flask, session, render_template_string, request, jsonify
import random
import operator
from concrete import fhe

app = Flask(__name__)
app.secret_key = 'aeirwairuefav8324fdsrawe3'

OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
}

# 產生簡單算術 CAPTCHA 題目
def generate_captcha():
    # 三個隨機整數
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    c = random.randint(1, 10)

    # a + b * c
    question = f"{a} + {b} * {c}"
    answer = a + (b * c)

    return question, a, b, c

def cmp(a, b, c, d):
    return a + b * c - d

compiler = fhe.Compiler(cmp, {"a": "encrypted", "b": "encrypted", "c": "encrypted", "d": "encrypted"})

inputset = [(x, y, z, x + y*z) for x in range(0, 20) for y in range(0, 20) for z in range(0, 20)]

print(f"Compilation...")
circuit = compiler.compile(inputset)

print(f"Key generation...")
circuit.keygen()

@app.route('/')
def index():
    question, a, b, c = generate_captcha()
    session['a'] = a
    session['b'] = b
    session['c'] = c
    html = '''
    <h1>請解答 CAPTCHA</h1>
    <p>{{ question }} = ?</p>
    <input id="answer" type="text">
    <button onclick="submitAnswer()">送出</button>
    <p id="result"></p>
    <script>
      async function submitAnswer() {
        let answer = document.getElementById('answer').value;
        let res = await fetch('/verify', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({answer})
        });
        let data = await res.json();
        document.getElementById('result').innerText = data.message;
      }
    </script>
    '''
    return render_template_string(html, question=question)

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    user_answer = int(data.get('answer'))
    #correct_answer = session.get('captcha_answer')
    a = session.get('a')
    b = session.get('b')
    c = session.get('c')
    print(f"Homomorphic evaluation...")
    encrypted_a, encrypted_b, encrypted_c, encrypted_d = circuit.encrypt(a, b, c, user_answer)
    encrypted_result = circuit.run(encrypted_a, encrypted_b, encrypted_c, encrypted_d)
    result = circuit.decrypt(encrypted_result)
    try:
        if result == 0:
            return jsonify({'message': '驗證成功'})
        else:
            return jsonify({'message': '驗證失敗'})
    except:
        return jsonify({'message': '輸入無效'})

if __name__ == '__main__':
    app.run(debug=True)

