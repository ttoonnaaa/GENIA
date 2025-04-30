from flask import Flask, render_template, request, jsonify
import json
import os
import google.generativeai as genai

# Load examples from JSON file
with open("last.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    data = json.load(f)
    examples = data["qa_pairs"]  # Access the 'qa_pairs' key

# Set your API key
api_key = "AIzaSyBzGRe__QBvML5BlljaydfWxT9sKki4ieE"
os.environ["GEMINI_API_KEY"] = api_key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 0.5,
    "top_p": 0.9,
    "top_k": 50,
    "max_output_tokens": 500,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

app = Flask(__name__)

def build_prompt(user_input):
    prompt = (
        "أنا مساعد في موقع يهتم بصحة المرأة الجسدية والنفسية. "
        "يمكنني تقديم استشارات طبية ونصائح حول مواضيع مثل الدورة الشهرية، السرطان، والدعم النفسي والاجتماعي.\n"
        "لكن يجب أن تعلمي أنني لست بديلاً عن الطبيب المختص. نصائحي مبنية على المعلومات المتاحة لي. يُنصح دائمًا بالتوجه لأطباء مختصين للحصول على مشورة طبية دقيقة.\n\n"
    )
    for pair in examples:
        prompt += f'المستخدم: {pair["question"]}\nالمساعد: {pair["answer"]}\n'
    prompt += f'المستخدم: {user_input}\nالمساعد:'
    return prompt

def chatbot_response(user_input):
    prompt = build_prompt(user_input)
    try:
        response = model.generate_content([prompt])
        if hasattr(response, 'text'):
            bot_output = response.text.strip()
        else:
            bot_output = "عذرًا، حدث خطأ غير متوقع."
        return bot_output
    except Exception as e:
        return f"عذرًا، حدث خطأ: {e}"

@app.route('/')
def index():
    return render_template('front.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    response = chatbot_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
