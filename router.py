from flask import Flask, render_template, request, jsonify
from text_analyses import TextAnalyzer
from text_modules_methods import fix_text, paraphrase_text  # Updated import

app = Flask(__name__)

text_analyzer = TextAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_text():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        analysis = text_analyzer.comprehensive_analysis(text)
        response = {
            'grammar': analysis.get('grammar', {}),
            'readability': analysis.get('readability', {}),
            'sentiment': analysis.get('sentiment', {}),
            'statistics': analysis.get('statistics', {}),
            'top_words': analysis.get('top_words', [])
        }
        return jsonify(response)
    except Exception as e:
        print(f"Analysis error: {e}")
        return jsonify({'error': 'Analysis failed', 'message': str(e)}), 500

@app.route('/fix', methods=['POST'])
def fix_text_endpoint():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        fixed_text = fix_text(text)
        return jsonify({
            'fixed_text': fixed_text,
            'suggestions': ['Fixed grammar and spelling'],
            'original_length': len(text),
            'fixed_length': len(fixed_text),
            'changes_made': fixed_text != text
        })
    except Exception as e:
        print(f"Fix error: {e}")
        return jsonify({'error': 'Fix failed', 'fixed_text': text}), 500

@app.route('/improve', methods=['POST'])
def improve_text_endpoint():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        improved_text = paraphrase_text(text)
        return jsonify({
            'improved_text': improved_text,
            'suggestions': ['Applied T5 paraphrasing'],
            'original_length': len(text),
            'improved_length': len(improved_text),
            'changes_made': improved_text != text
        })
    except Exception as e:
        print(f"Improve error: {e}")
        return jsonify({'error': 'Improve failed', 'improved_text': text}), 500

if __name__ == '__main__':
    print("Starting Text Analysis & Writing Assistant...")
    print("Visit: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)