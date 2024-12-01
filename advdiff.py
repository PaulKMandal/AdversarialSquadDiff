import difflib
from datasets import load_dataset
from termcolor import colored  # Library to print colored text in the console

# Hardcoded sample data for testing
"""
original_squad = [
    {
        'id': '1',
        'context': "The quick brown fox jumps over the lazy dog.",
        'question': "What does the fox do?",
        'answers': {
            'text': ["jumps over the lazy dog"],
            'answer_start': [16]
        }
    },
    {
        'id': '2',
        'context': "Python is a widely used high-level programming language.",
        'question': "What type of language is Python?",
        'answers': {
            'text': ["high-level programming language"],
            'answer_start': [24]
        }
    },
    {
        'id': '3',
        'context': "Machine learning provides systems the ability to automatically learn.",
        'question': "What does machine learning provide?",
        'answers': {
            'text': ["the ability to automatically learn"],
            'answer_start': [26]
        }
    }
]

adversarial_squad = [
    {
        'id': '1',
        'context': "The quick brown fox leaps over the lazy dog.",
        'question': "What does the fox do?",
        'answers': {
            'text': ["leaps over the lazy dog"],
            'answer_start': [16]
        }
    },
    {
        'id': '2',
        'context': "Python is a widely used programming language.",
        'question': "What type of language is Python?",
        'answers': {
            'text': ["programming language"],
            'answer_start': [24]
        }
    },
    {
        'id': '3',
        'context': "Machine learning gives systems the ability to automatically learn.",
        'question': "What does machine learning provide?",
        'answers': {
            'text': ["the ability to automatically learn"],
            'answer_start': [26]
        }
    }
]
"""

# Load the original SQuAD dataset
original_squad = load_dataset('squad', split='validation')

# Load the adversarial SQuAD dataset (choose 'AddSent' or 'AddOneSent')
adversarial_squad = load_dataset('squad_adversarial', 'AddSent', split='validation')

# Create a mapping from id to example in the original dataset
original_squad_dict = {example['id']: example for example in original_squad}

# Counter to limit output for demonstration
diff_count = 0
max_diffs_to_show = 10  # Adjust as needed

def highlight_differences(a, b):
    import difflib
    from termcolor import colored
    
    # Compute the diffs between the two strings
    s = difflib.SequenceMatcher(None, a, b)
    output_a = []
    output_b = []
    
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == 'equal':
            output_a.append(a[i1:i2])
            output_b.append(b[j1:j2])
        elif tag == 'replace':
            output_a.append(colored(a[i1:i2], 'red'))
            output_b.append(colored(b[j1:j2], 'green'))
        elif tag == 'delete':
            output_a.append(colored(a[i1:i2], 'red'))
        elif tag == 'insert':
            output_b.append(colored(b[j1:j2], 'green'))
    return ''.join(output_a), ''.join(output_b)

# Iterate over adversarial examples
for example in adversarial_squad:
    id_ = example['id']
    original_example = original_squad_dict.get(id_)
    if original_example:
        fields = ['title', 'context', 'question']
        differences_found = False
        print(f"ID: {id_}")
        for field in fields:
            original_value = original_example.get(field, '')
            adversarial_value = example.get(field, '')
            if original_value != adversarial_value:
                highlighted_original, highlighted_adversarial = highlight_differences(original_value, adversarial_value)
                print(f"\nField: {field}")
                print("Original:")
                print(highlighted_original)
                print("Modified:")
                print(highlighted_adversarial)
                differences_found = True
        # Compare answers
        original_answers = original_example.get('answers', {})
        adversarial_answers = example.get('answers', {})
        # Compare 'text' field in answers
        original_texts = original_answers.get('text', [])
        adversarial_texts = adversarial_answers.get('text', [])
        for idx in range(max(len(original_texts), len(adversarial_texts))):
            original_text = original_texts[idx] if idx < len(original_texts) else ''
            adversarial_text = adversarial_texts[idx] if idx < len(adversarial_texts) else ''
            if original_text != adversarial_text:
                highlighted_original, highlighted_adversarial = highlight_differences(original_text, adversarial_text)
                print(f"\nAnswer Text {idx+1}:")
                print("Original:")
                print(highlighted_original)
                print("Modified:")
                print(highlighted_adversarial)
                differences_found = True
        # Compare 'answer_start' field in answers
        original_starts = original_answers.get('answer_start', [])
        adversarial_starts = adversarial_answers.get('answer_start', [])
        for idx in range(max(len(original_starts), len(adversarial_starts))):
            original_start = str(original_starts[idx]) if idx < len(original_starts) else ''
            adversarial_start = str(adversarial_starts[idx]) if idx < len(adversarial_starts) else ''
            if original_start != adversarial_start:
                highlighted_original, highlighted_adversarial = highlight_differences(original_start, adversarial_start)
                print(f"\nAnswer Start {idx+1}:")
                print("Original:")
                print(highlighted_original)
                print("Modified:")
                print(highlighted_adversarial)
                differences_found = True
        if differences_found:
            print("\n" + "="*80 + "\n")
            diff_count += 1
            if diff_count >= max_diffs_to_show:
                break

print(f"Total differences found: {diff_count}")
if diff_count == 0:
    print("No differences found between the contexts.")
