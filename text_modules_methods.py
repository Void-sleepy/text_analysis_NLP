from text_improver import load_grammar_model, load_paraphraser_model, lang_tool

def fix_text(text):
    try:
        grammar_model = load_grammar_model()
        if grammar_model:
            prompt = f"{text}"
            corrected = grammar_model(
                prompt, 
                max_length=min(len(text) + 100, 512),
                do_sample=False
            )[0]['generated_text']

            if lang_tool:
                corrected = lang_tool.correct(corrected)

            return corrected
        else:
            print("Grammar model not available.")
            return text
    except Exception as e:
        print(f"Grammar model error: {e}")
        return text

def paraphrase_text(text):
    """Paraphrase text for better style"""
    try:
        paraphraser_model = load_paraphraser_model()
        if paraphraser_model:
            paraphrased = paraphraser_model(
                f"paraphrase: {text}", 
                max_length=min(len(text) + 100, 512),
                do_sample=False
            )[0]['generated_text']

            if paraphrased.lower() != text.lower() and len(paraphrased) > 10:
                return paraphrased
            else:
                print("Paraphraser returned unchanged text, using original")
                return text
        else:
            print("Paraphraser model not available")
            return text
    except Exception as e:
        print(f"Paraphraser model error: {e}")
        return text

def fix_and_paraphrase(text):
    corrected = fix_text(text)
    if len(corrected.split()) > 12:
        paraphrased = paraphrase_text(corrected)
        return {
            "fixed": corrected,
            "paraphrased": paraphrased
        }
    return {
        "fixed": corrected,
        "paraphrased": None
    }