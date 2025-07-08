# text_improver.py (Fixed with Proper Caching and Error Handling)

import re
import nltk
import torch
from transformers import pipeline
import language_tool_python

# Ensure NLTK tokenizers are downloaded
nltk.download('punkt', quiet=True)

# ─── gpu 

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
if torch.cuda.is_available():
    print(f"Using GPU: {torch.cuda.get_device_name(0)}")
else:
    print("Using CPU")
device_index = 0 if torch.cuda.is_available() else -1

try:
    lang_tool = language_tool_python.LanguageTool('en-US')
    print("Language Tool loaded")
except Exception as e:
    print(f"Language Tool failed: {e}")
    lang_tool = None

grammar_model = None
paraphraser_model = None

# ─── Efficient Model Loaders ────────────────────────────────

def load_grammar_model():
    """Load grammar model with caching"""
    global grammar_model
    if grammar_model is None:
        try:
            print("Loading grammar model...")
            grammar_model = pipeline(
                "text2text-generation",
                model="pszemraj/flan-t5-large-grammar-synthesis",
                framework="pt",
                device=device_index,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            )
            print("Grammar model loaded")
        except Exception as e:
            print(f"Grammar model failed: {e}")
            grammar_model = "failed"
    return grammar_model if grammar_model != "failed" else None







def load_paraphraser_model():
    """Load paraphraser model with caching"""
    global paraphraser_model
    if paraphraser_model is None:
        try:
            print("Loading paraphraser model...")
            paraphraser_model = pipeline(
                "text2text-generation",
                model="Vamsi/T5_Paraphrase_Paws",
                framework="pt",
                device=device_index,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            )
            print("Paraphraser model loaded")
        except Exception as e:
            print(f"Paraphraser model failed: {e}")
            paraphraser_model = "failed"
    return paraphraser_model if paraphraser_model != "failed" else None