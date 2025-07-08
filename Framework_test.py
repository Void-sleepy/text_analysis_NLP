#!/usr/bin/env python3
"""
Interactive test script for the text analysis and improvement pipeline.
Run this to test different text samples and see the analysis results.
"""

import sys
import os

def load_test_samples():
    """Load test samples from the test file"""
    samples = {}
    current_sample = None
    current_text = []
    
    try:
        with open('test_samples.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('## Sample'):
                    # Save previous sample
                    if current_sample and current_text:
                        samples[current_sample] = '\n'.join(current_text).strip()
                    
                    # Start new sample
                    current_sample = line.replace('## ', '').replace(':', '')
                    current_text = []
                elif line and not line.startswith('#'):
                    current_text.append(line)
            
            # Save last sample
            if current_sample and current_text:
                samples[current_sample] = '\n'.join(current_text).strip()
                
    except FileNotFoundError:
        print("❌ test_samples.txt not found. Please make sure it's in the current directory.")
        return {}
    
    return samples

def analyze_sample(text, sample_name):
    """Analyze a text sample and display results"""
    try:
        from text_analyses import TextAnalyzer
        from text_improver import TextImprover
        
        print(f"\n{'='*60}")
        print(f"ANALYZING: {sample_name}")
        print(f"{'='*60}")
        print(f"Text: {text[:200]}{'...' if len(text) > 200 else ''}")
        print(f"Length: {len(text)} characters, {len(text.split())} words")
        
        # Initialize analyzers
        analyzer = TextAnalyzer()
        improver = TextImprover()
        
        # Perform analysis
        print("\n📊 Running comprehensive analysis...")
        analysis = analyzer.comprehensive_analysis(text)
        
        # Display key metrics
        print("\n📈 KEY METRICS:")
        if 'readability' in analysis:
            fre = analysis['readability'].get('flesch_reading_ease', 0)
            level = analysis['readability'].get('readability_level', 'unknown')
            print(f"  • Reading Ease: {fre:.1f} ({level})")
        
        if 'grammar' in analysis:
            issues = analysis['grammar'].get('total_issues', 0)
            print(f"  • Grammar Issues: {issues}")
        
        if 'sentiment' in analysis:
            sentiment = analysis['sentiment'].get('overall_sentiment', 'unknown')
            subjectivity = analysis['sentiment'].get('textblob_sentiment', {}).get('subjectivity', 0)
            print(f"  • Sentiment: {sentiment} (Subjectivity: {subjectivity:.2f})")
        
        if 'statistics' in analysis:
            words = analysis['statistics'].get('word_count', 0)
            sentences = analysis['statistics'].get('sentence_count', 0)
            avg_length = analysis['statistics'].get('avg_words_per_sentence', 0)
            print(f"  • Structure: {words} words, {sentences} sentences (avg: {avg_length:.1f} words/sentence)")
        
        # Generate suggestions
        print("\n💡 IMPROVEMENT SUGGESTIONS:")
        suggestions = improver.generate_all_suggestions(text, analysis)
        
        if suggestions:
            for i, suggestion in enumerate(suggestions[:5], 1):  # Show top 5
                priority = suggestion.get('priority', 'low').upper()
                category = suggestion.get('category', 'Unknown')
                issue = suggestion.get('issue', 'No issue specified')
                print(f"  {i}. [{priority}] {category}: {issue}")
        else:
            print("  ✅ No improvement suggestions - text looks good!")
        
        # Show grammar issues if any
        if 'grammar' in analysis and analysis['grammar'].get('issues'):
            print(f"\n🔍 GRAMMAR ISSUES (showing first 3):")
            for i, issue in enumerate(analysis['grammar']['issues'][:3], 1):
                severity = issue.get('severity', 'unknown').upper()
                message = issue.get('message', 'No message')
                print(f"  {i}. [{severity}] {message}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR analyzing text: {e}")
        import traceback
        traceback.print_exc()
        return False

def interactive_test():
    """Run interactive testing session"""
    print("🔬 TEXT ANALYSIS & IMPROVEMENT PIPELINE TESTER")
    print("=" * 50)
    
    # Load samples
    samples = load_test_samples()
    if not samples:
        print("No test samples available.")
        return
    
    while True:
        print(f"\n📝 AVAILABLE TEST SAMPLES:")
        sample_list = list(samples.keys())
        for i, sample_name in enumerate(sample_list, 1):
            print(f"  {i}. {sample_name}")
        
        print(f"  {len(sample_list) + 1}. Enter custom text")
        print(f"  {len(sample_list) + 2}. Test all samples")
        print("  0. Exit")
        
        try:
            choice = input(f"\nSelect option (0-{len(sample_list) + 2}): ").strip()
            
            if choice == '0':
                print("👋 Goodbye!")
                break
            elif choice == str(len(sample_list) + 1):
                # Custom text
                print("\nEnter your text (press Enter twice to finish):")
                lines = []
                while True:
                    line = input()
                    if line == "" and lines:
                        break
                    lines.append(line)
                
                if lines:
                    custom_text = '\n'.join(lines)
                    analyze_sample(custom_text, "Custom Text")
                else:
                    print("No text entered.")
                    
            elif choice == str(len(sample_list) + 2):
                # Test all samples
                print("\n🚀 Testing all samples...")
                for sample_name, text in samples.items():
                    analyze_sample(text, sample_name)
                    input("\nPress Enter to continue to next sample...")
                    
            elif choice.isdigit() and 1 <= int(choice) <= len(sample_list):
                # Test specific sample
                idx = int(choice) - 1
                sample_name = sample_list[idx]
                text = samples[sample_name]
                analyze_sample(text, sample_name)
                
            else:
                print("❌ Invalid choice. Please try again.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Check if modules are available
    try:
        from text_analyses import TextAnalyzer
        from text_improver import TextImprover
        print("✅ Text analysis modules loaded successfully!")
    except ImportError as e:
        print(f"❌ Failed to import modules: {e}")
        print("Please ensure text_analyses.py and text_improver.py are in the current directory.")
        sys.exit(1)
    
    interactive_test()
