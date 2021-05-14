import pickle

stopwords = {'per', '’ll', 'could', 'fifteen', 'been', "isn't", 'whoever', 'any', 'whole', 'front', "won't", 'upon', 'there', 's', 'am', 'via', 'the', 'as', "haven't", 'on', 'km', 'further', 'their', 'quite', 'have', 'twenty', 'during', 'full', 'it', 'thin', 'so', 'what', 'an', 't', 'less', 'if', 'sixty', 'everyone', 'us', 'were', 'side', 'she', 'cannot', 'thereby', '‘ve', 'amount', 'n’t', 'be', 'nine', 'isn', 'wouldn', 'by', 'along', "'ll", 'themselves', 'forty', 'everywhere', "'d", 'thru', 'sometimes', 'hasnt', 'seeming', 'own', 'that', "'ve", 'least', 'with', 'inc', 'really', 'afterwards', 'due', 'for', 'sometime', 'last', 'find', 'therein', 'all', 'thick', 'detail', 'few', 'hundred', 'some', 'even', 'off', '’m', 'ain', '’re', 'hence', 'etc', 'into', 'rather', 'where', 'm', 'its', 'onto', '’s', 'get', 'other', 'moreover', 'noone', 'being', 'must', 'bill', "wasn't", 'system', 'neither', "you'll", 'third', 'whereby', 'nobody', 'among', 'throughout', 'except', 'beforehand', "didn't", 'was', 'without', 'whose', 'hasn', '‘d', 'or', 'theirs', 'various', 'name', 'twelve', 'myself', 'former', 'though', 'we', 'ours', 'many', 'sincere', 'regarding', 'had', 'before', 'mustn', 'either', 'doing', 'why', 'fill', 'eight', 'won', 'anything', 'hereupon', 'this', 'amoungst', '‘s', 'of', 'yourselves', 'beside', 'within', 'ourselves', '‘re', 'about', 'elsewhere', 'latter', 'through', 'll', 'i', 'wasn', 'anywhere', 'weren', 'just', 'itself', "you're", 'wherein', 'four', 'keep', 'whether', 'nothing', 'found', 'back', 'needn', "aren't", 'has', 'one', 'wherever', 'serious', 'everything', 'hadn', 'first', 'anyway', 'co', 'still', 'five', 'becomes', "don't", 'formerly', 'ever', 'part', 'nowhere', 'made', 'himself',  "couldn't", 'none', 'others', 'now', 'doesn', 'at', 'another', 'does', 'kg', 'see', 'often', 'them', 'shan', 'fifty', 'ltd', 'namely', 'they', 'somewhere', 'haven', 'take', 'latterly', 'well', 'whatever', 'nor', 'whereafter', 'might', 'only', 'de', 'our', 'hers', "mustn't", 'aren', 'you', 'his', "wouldn't", 'please', 'empty', 'but', 'mightn', 'then', 'should', 'and', 'each', 'such', 'a', 'yet', 'y', 'enough', 'someone', 'would', 'since', 'however', 'make', 'alone', 'anyone', 'amongst', 'these', 'whereupon', 'fire', "hasn't", 'shouldn', 'didn', 'do', 'me', 'becoming', 'after', 'several', 'seem', 'her', 'three', 'out', 'ten', 'whence', 'eg', 'couldn', 'un', 'did', "she's", 'whither', 'toward', 'once', "should've", 'call', "weren't", 'again', 'more', 'show', 'seems', "needn't", 'thereupon', 'used', 'most', 'hereby', 'put', 'ie', 've', 'my', 'your', 'thence', 'already', 'always', 'having', 'much', 'move', 'eleven', "'re", 'here', 'yours', 'con', 'done', 'up', 'over', 'yourself', "it's", 'o', 'six', 'can', 'how', "hadn't", 'anyhow', 'below', 'also', 'say', 'together', 'down', 'using', 'while', 'almost', 'cry', "you've", '’ve', 'two', 'towards', 'meanwhile', 'perhaps', 'when', 'ma', "shouldn't", 'both', 'hereafter', 'he', 'describe', 'ca', 'which', 'every', 'between', 'give', 'go', 'very', '’d', 'nevertheless', 'is', 'n‘t', 'therefore', '‘ll', 'unless', 'next', 'who', 'became', 'mill', 'him', 'don', 'same', "'s", 'seemed', 'mostly', 'will', 're', "you'd", 'no', 'in', 'too', "mightn't", 'besides', 'are', 'because', 'couldnt', 'd', 'against', "doesn't", 'cant', 'whenever', 'somehow', 'thereafter', 'although', 'beyond', 'from', 'whereas', 'thus', 'than', "shan't", 'to', 'top', 'until', 'those', 'whom', 'bottom', 'else', 'herein', 'something', '‘m', 'may', 'not', "that'll", "'m", 'indeed', 'never', 'herself', 'interest', "n't", 'become', 'mine', 'otherwise'}
punctuations = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', ' ', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
NOT_GROUNDED_OBJECTS_WORDS = {'photo', 'image', 'picture', 'pic', 'side', 'part', 'background'}
stopwords_and_punctuations = stopwords.union(punctuations)
stopwords_and_punctuations = stopwords_and_punctuations.union(NOT_GROUNDED_OBJECTS_WORDS)

from collections import Counter
print(f"stopwords: {len(stopwords)}, punctuations: {len(punctuations)}, stopwords_and_punctuations: {len(stopwords_and_punctuations)}")
MY_RELATIONSHIP_MASKS = ['VERB', 'ADP']
TOP_COMMON_RELATIONSHIPS = ['on', 'of', 'in', 'and', 'with', 'to', 'or', 'at', 'by', 'as']
MY_OBJECT_MASKS = ['NOUN']
MY_ATTRIBUTES_MASKS = ['ADJ']
my_definite_attributes_list = ['white', 'black', 'green', 'blue', 'brown', 'gray', 'large', 'small', 'wood', 'yellow', 'tall', 'metal', 'long', 'dark', 'silver', 'pink', 'round', 'short', 'plastic', 'tan', 'purple', 'colorful', 'concrete', 'blond', 'young', 'empty', 'happy', 'bright', 'wet', 'gold', 'dirty', 'shiny', 'square', 'thin', 'little', 'leafy', 'thick', 'beige', 'calm', 'rectangular', 'dry', 'leather', 'snowy', 'pointy', 'fluffy', 'clean', 'plaid', 'electric', 'grassy', 'lit', 'blurry', 'leafless', 'flat', 'decorative', 'beautiful', 'sandy', 'steel', 'overcast', 'wide', 'stainless', 'ceramic', 'rusty', 'furry', 'ripe', 'hazy', 'high', 'cloudless', 'fresh', 'tiny', 'huge', 'skinny', 'rocky', 'curly', 'maroon', 'porcelain', 'lush', 'floral', 'reflective', 'iron', 'bald', 'rubber', 'puffy', 'broken', 'chrome', 'smooth', 'evergreen', 'low', 'narrow', 'denim', 'hardwood', 'wicker', 'straight', 'triangular', 'sunny', 'bushy', 'hairy', 'wavy', 'khaki', 'shirtless', 'marble', 'ornate', 'overhead', 'muddy', 'fuzzy', 'burnt', 'wild', 'rough', 'sharp', 'pale', 'floppy', 'barefoot', 'plain', 'delicious', 'healthy', 'soft', 'choppy', 'neon', 'aluminum', 'knit', 'wispy', 'vertical', 'patchy', 'granite', 'messy', 'pretty', 'deep', 'sleeveless', 'fallen', 'modern', 'murky', 'antique', 'heavy', 'fancy', 'transparent', 'teal', 'vintage', 'horizontal', 'gravel', 'octagonal', 'sparse', 'cotton', 'shallow', 'fat', 'overgrown', 'foggy', 'giant', 'barren', 'shaggy', 'dusty', 'wireless', 'plush', 'mesh', 'warm', 'woven', 'raw', 'clay', 'brass', 'foamy', 'brunette', 'copper', 'athletic', 'spread', 'crispy', 'unripe', 'styrofoam', 'sheer', 'palm', 'grey', 'golden', 'wooden', 'blonde', 'bloody', "striped", "arched", "checkered", "patterned", "piled", "wrinkled", "stuffed", "decorated", "rounded", "rolled", "grilled"]

all_objects_attributes_relationships = pickle.load(open('all_objects_attributes_relationships.pickle', 'rb'))

objects_list = [x for x in all_objects_attributes_relationships['objects']['joint'] if len(x.split(" ")) == 1]
attributes_list = [x for x in all_objects_attributes_relationships['attributes']['joint'] if len(x.split(" ")) == 1]
relationships_list = [x for x in all_objects_attributes_relationships['relationships']['joint'] if len(x.split(" ")) == 1]
print(f"Loaded objects_list, # {len(objects_list)}")
print(f"Loaded attributes_list, # {len(attributes_list)}")
print(f"Loaded relationships_list, # {len(relationships_list)}")

def is_content_word(token, pos=None, lemma=None):
    return token.lower() not in stopwords_and_punctuations and len(token) > 1

def is_object(word, pos, lemma=None):
    return pos in MY_OBJECT_MASKS and word not in stopwords_and_punctuations and \
           len(word) > 1 and (word in objects_list or lemma in objects_list)

def is_relationship(word, pos, lemma):
    return (word in relationships_list or lemma in relationships_list) and pos in MY_RELATIONSHIP_MASKS

def is_attribute(word, pos, lemma):
    if word in my_definite_attributes_list:
        return True
    else:
        return (word in attributes_list or lemma in attributes_list) and pos in MY_ATTRIBUTES_MASKS


token_is_relevant_for_masking_strategy = {'sw': is_content_word, 'obj': is_object, 'att': is_attribute, 'rel': is_relationship, }
