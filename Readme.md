## PageRank Implementation  

### Assumptions -  
1. The window is assumed to move w spaces and not by 1 space. For example, if a file has 10 words and window size is 5, we will have two windows of first five and the next five words.   
2. The words that remain in a window (if it matches the POS tag type and removing the stopwords) have edges between them in the graph. If another window has a same word which was present in the previous window, then we wont create a new node for it. Instead we'll use the previously created node for adding the new edges.  
3. The original text is considered for creating the n-grams.    

### Functionality of the code -  

1. class graph_node :- For creating node instances of the graph. Each node holds a word, its edges with edge weights, page-rank score and total adjacent edge weights.  
2. parseStopwords :- Stores the words from stopwords.txt file into a list.  
3. tokenizer :- Used to convert a word to lower case and then split it on blank spaces. It return a list.  
4. tagSeparator :- Separates the tokenized words into text and tag by making use of the POS tags that are appended to it.  
5. stemAndCheck :- Used to stem a word using NLTK's Porter Stemmer and remove it if it's a stopword.  
6. addToGraph :- Add new nodes to a graph if the list of words contains new words. Adds new edges amongst the words in the list. Ignores the ' ' strings.  
7. computePageRank :- Used to assign a page-rank score to the nodes of the graph. Damping factor of 0.85 and max iteration count of 10 are used.   
8. topK_Ngrams :- Given unigrams, bigrams and trigrams, this function returns the top-k N-grams by sorting the summation of page-rank scores for all words of an n-gram.  
9. preprocessGold :- Returns a list of stemmed phrases from the gold file.  
10. findRank :- Matches the top-k n-grams with the list of phrases from the corresponding gold file. If a match is found, the corresponding k value of the n-gram is returned as a rank for that document, else it returns a zero.  
11. readDatasetAndCompute :- Used to parse the abstracts dataset and the gold dataset and to call all the other relevant functions in order to compute the page-rank of graphs for each document and the Mean Reciprocal Rank of the top-k N-grams of all documents.  

### How to run the code -  

For Windows:-  
1. Open Command prompt:   Start menu -> Run  and type 'cmd'. This will cause the Windows terminal to open.  
2. Type 'cd ' followed by project directory path to change current working directory, and hit Enter.   
3. Run the program using command 'python page_rank.py'  
4. You will be prompted to input the paths to the abstracts dataset directory, gold dataset directory, stopwords file and the length of window(window size).   
Alternatively, you can also use an IDE of your choice to execute the code.  

For Mac:-  
1. Open Terminal by searching it using the search icon at top right or through 'Launchpad->Other->Terminal'   
2. Type 'cd ' followed by project directory path to change current working directory, and hit Enter.   
3. Run the program using command 'python3 page_rank.py'  
4. You will be prompted to input the paths to the abstracts dataset directory, gold dataset directory, stopwords file and the length of window(window size).  

### Output -   

Enter the path to the abstracts dataset directory/folder: www/abstracts  

Enter the path to the gold dataset directory/folder: www/gold  

Enter the path to the stopwords file: stopwords.txt  

Enter the size of the window "w": 6  

The computed MRR@k values for w=6 are:   

At k = 1: 0.07293233082706767  
At k = 2: 0.10563909774436091  
At k = 3: 0.13045112781954893  
At k = 4: 0.15000000000000013  
At k = 5: 0.16548872180451105  
At k = 6: 0.17714285714285663  
At k = 7: 0.18433941997851705  
At k = 8: 0.18866272824919372  
At k = 9: 0.19325754863348787  
At k = 10: 0.19618987946055547  