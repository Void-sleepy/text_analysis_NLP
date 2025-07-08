import re
import nltk
from textstat import flesch_reading_ease, flesch_kincaid_grade, automated_readability_index
from textblob import TextBlob
from collections import Counter
from nltk.tokenize import word_tokenize

try:
    nltk.download('punkt', quiet=True)
except:
    pass

WEAK_WORDS = [
    'very', 'really', 'quite', 'rather', 'pretty', 'kind of', 'sort of',
    'basically', 'actually', 'just', 'somewhat', 'fairly', 'almost', 'seemingly',
    'literally', 'totally', 'absolutely', 'completely', 'entirely'
]

ACADEMIC_REPLACEMENTS = {
    'show': 'demonstrate', 'big': 'significant', 'small': 'minimal',
    'good': 'effective', 'bad': 'ineffective', 'get': 'obtain',
    'use': 'utilize', 'help': 'facilitate'
}
REDUNDANT_PHRASES = {
    'in order to': 'to', 'due to the fact that': 'because',
    'at this point in time': 'now', 'in the event that': 'if',
    'for the purpose of': 'to'
}

STOP_WORDS = set([
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
    'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must',
    'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
])

class TextAnalyzer:
    def analyze_readability(self, text):
        if len(text.strip()) < 10:
            return {
                'flesch_score': 0,
                'grade_level': 'N/A',
                'readability_level': 'Insufficient text'
            }

        try:
            flesch_score = flesch_reading_ease(text)
            grade_level = flesch_kincaid_grade(text)
            return {
                'flesch_score': round(flesch_score, 1),
                'grade_level': round(grade_level, 1),
                'readability_level': self._get_readability_level(flesch_score)
            }
        except Exception as e:
            return {
                'flesch_score': 0,
                'grade_level': 'Error',
                'readability_level': 'Analysis failed'
            }

    def analyze_sentiment(self, text):
        """Analyze sentiment and tone"""
        try:
            blob = TextBlob(text)
            sentiment = blob.sentiment

            if sentiment.polarity > 0.1:
                overall_tone = 'Positive'
            elif sentiment.polarity < -0.1:
                overall_tone = 'Negative'
            else:
                overall_tone = 'Neutral'

            academic_score = self._score_academic_style(text)
            academic_level = self._academic_level(academic_score)

            return {
                'polarity': round(sentiment.polarity, 3),
                'subjectivity': round(sentiment.subjectivity, 3),
                'overall_tone': overall_tone,
                'academic_level': academic_level.title()
            }
        except Exception as e:
            return {
                'polarity': 0,
                'subjectivity': 0,
                'overall_tone': 'Unknown',
                'academic_level': 'Unknown'
            }

    def analyze_grammar(self, text):
        """Analyze grammar and style issues"""
        issues = []
        style_suggestions = []
        
        # repeated words ?
        repeated = re.findall(r'\b(\w+)\s+\1\b', text, re.IGNORECASE)
        for word in repeated:
            issues.append({'message': f'Repeated word: "{word}"', 'type': 'grammar'})
        
        # weak words ? 
        for weak_word in WEAK_WORDS:
            if re.search(rf'\b{weak_word}\b', text, re.IGNORECASE):
                style_suggestions.append({'message': f'Consider stronger alternative to "{weak_word}"', 'type': 'style'})
        
        return {
            'issues': issues,
            'style_suggestions': style_suggestions
        }

    def get_statistics(self, text):
        """Get basic text statistics"""
        try:
            words = word_tokenize(text)
            words = [word for word in words if word.isalpha()]
            sentences = nltk.sent_tokenize(text)
            return {
                'word_count': len(words),
                'sentence_count': len(sentences),
                'character_count': len(text),
                'avg_words_per_sentence': round(len(words) / len(sentences), 1) if sentences else 0
            }
        except Exception as e:
            return {
                'word_count': 0,
                'sentence_count': 0,
                'character_count': len(text),
                'avg_words_per_sentence': 0
            }

    def get_word_frequency(self, text):
        """Get most common words"""
        try:
            words = word_tokenize(text.lower())
            filtered = [w for w in words if w.isalpha() and w not in STOP_WORDS and len(w) > 2]
            return Counter(filtered).most_common(10)
        except:
            return []

    def comprehensive_analysis(self, text):
        """Perform complete text analysis"""
        if not text or not text.strip():
            return {
                'error': 'No text provided',
                'grammar': {'issues': [], 'style_suggestions': []},
                'readability': {'flesch_score': 0, 'grade_level': 'N/A', 'readability_level': 'N/A'},
                'sentiment': {'overall_tone': 'N/A', 'academic_level': 'N/A'},
                'statistics': {'word_count': 0, 'sentence_count': 0, 'character_count': 0},
                'top_words': []
            }

        try:
            return {
                'grammar': self.analyze_grammar(text),
                'readability': self.analyze_readability(text),
                'sentiment': self.analyze_sentiment(text),
                'statistics': self.get_statistics(text),
                'top_words': self.get_word_frequency(text),
                'success': True
            }
        except Exception as e:
            print(f"Analysis error: {e}")
            return {
                'error': f'Analysis failed: {str(e)}',
                'grammar': {'issues': [], 'style_suggestions': []},
                'readability': {'flesch_score': 0, 'grade_level': 'Error', 'readability_level': 'Error'},
                'sentiment': {'overall_tone': 'Error', 'academic_level': 'Error'},
                'statistics': {'word_count': 0, 'sentence_count': 0, 'character_count': len(text)},
                'top_words': []
            }

    def _get_readability_level(self, flesch_score):
        if flesch_score >= 90:
            return "Very Easy"
        elif flesch_score >= 80:
            return "Easy"
        elif flesch_score >= 70:
            return "Fairly Easy"
        elif flesch_score >= 60:
            return "Standard"
        elif flesch_score >= 50:
            return "Fairly Difficult"
        elif flesch_score >= 30:
            return "Difficult"
        else:
            return "Very Difficult"

    def _score_academic_style(self, text):
        score = 0
        academic_words = [  
            'research', 'study', 'analysis', 'evidence', 'methodology', 'conclusion', 'significant',
            'objective', 'evaluate', 'framework', 'approach', 'systematic', 'demonstrate', 'impact',
            'theory', 'variable', 'experiment', 'finding', 'result', 'indicate', 'data', 'interpret',
            'investigate', 'observe', 'support', 'hypothesis', 'outcome', 'critical', 'academic',
            'discuss', 'elaborate', 'context', 'construct', 'structure', 'compare', 'correlation'
        ]
        informal_words = [  
            'awesome', 'amazing', 'cool', 'totally', 'lol', 'omg', 'kinda', 'yep', 'nah', 'wanna',
            'gonna', 'stuff', 'things', 'like', 'idk', 'bruh', 'literally', 'basically', 'dude',
            'super', 'heck', 'ya', 'btw', 'pls', 'meh', 'whatever', 'nope', 'lmao', 'haha'
        ]

        words = [word.lower() for word in word_tokenize(text) if word.isalpha()]

        for word in academic_words:
            score += words.count(word) * 2
        for word in informal_words:
            score -= words.count(word) * 3

        if score <= 0 and len(words) > 25 and not any(w in words for w in informal_words):
            score = 3

        return score

    def _academic_level(self, score):
        if score > 10:
            return 'high'
        elif score > 3:
            return 'medium'
        elif score > 0:
            return 'low'
        else:
            return 'informal'

