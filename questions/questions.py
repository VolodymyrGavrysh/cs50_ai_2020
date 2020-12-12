import nltk
import sys
from nltk.corpus import stopwords
# nltk.download('stopwords')
import string, math, os



FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    res = dict()

    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if file.endswith('.txt'):
            
            try:
                with open(file_path, 'r') as f:
                    res[file] = f.read()
            except Exception as e:
                print(f'Problem with {file}')
                print(str(e))
    print(f"Loaded files from {directory}")
    print()
    return res

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # remove puckt
    # print('start tokenize')

    # table = str.maketrans(dict.fromkeys(string.punctuation))
    # new_s = document.translate(table) 
    
    tokens = nltk.word_tokenize(document)
    stop = stopwords.words("english")

    return [word.lower() for word in tokens if not all(f in string.punctuation for f in word) and word.lower() not in stop]


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    # print('start compute_idfs')

    total_num_of_documents = len(documents.keys())
    
    idfs_dict = dict()
    
    list_of_all_words = set([one for two in documents.values() for one in two])

    for words in list_of_all_words:
        number_word_appear = 0
        
        for word in documents.values():
            if words in word:
                number_word_appear += 1
                
        value_idf = math.log(total_num_of_documents / number_word_appear)
        
        idfs_dict[words] = value_idf
            
    return idfs_dict

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    score = {name: 0 for name in files}
        
    for file, words in files.items():

        for word in query:

            score[file] += words.count(word) * idfs[word]
        
    # score = sorted(score.items(), key=lambda x: x[1])

    return [k for k, v in sorted(score.items(), key=lambda item: item[1], reverse=True)][:n]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    score = {name: [0, 0] for name in sentences}
    
    for word in query:
        
        for sentence, words in sentences.items():

            if word in words:
                
                score[sentence][0] += idfs[word]
                
                score[sentence][1] += words.count(word) / len(words)


    score = sorted(score, key=lambda x: (score[x][0], score[x][1]), reverse=True)
                
    return score[:n]


if __name__ == "__main__":
    main()
