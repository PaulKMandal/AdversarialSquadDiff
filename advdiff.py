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
adversarial_squad = load_dataset('squad_adversarial', 'AddOneSent', split='validation')

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
        original_context = original_example['context']
        adversarial_context = example['context']

        # Skip if contexts are identical
        if original_context == adversarial_context:
            continue

        # Check if the only difference is whitespace
        if original_context.strip() == adversarial_context.strip():
            continue

        # Highlight differences
        highlighted_original, highlighted_adversarial = highlight_differences(original_context, adversarial_context)

        print(f"ID: {id_}")
        print("Original Context:")
        print(highlighted_original)
        print("\nModified Context:")
        print(highlighted_adversarial)
        print("\n" + "="*80 + "\n")
        diff_count += 1
        if diff_count >= max_diffs_to_show:
            break

print(f"Total differences found: {diff_count}")
if diff_count == 0:
    print("No differences found between the contexts.")
