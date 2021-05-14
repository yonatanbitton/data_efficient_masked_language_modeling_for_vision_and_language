import heapq
import random

from src.semantic_types_information import stopwords_and_punctuations, is_content_word, is_object


def random_word_objects(tokens, tokenizer, original_sent, pos_cache):
    """
    Masking strategy: Objects. Chooses 1 object to mask.
    :param tokens: same argument as original random_word function.
    :param tokenizer: the BertTokenizer used for the original implementation.
    :param original_sent: The sentence.
    :param max_seq_length: Maximum sequence length of the model (20 in the original implementation).
    :param pos_cache: A cache to hold the word, pos tag, lemma
    :return: (list of str, list of int), masked tokens and related labels for LM prediction
    """
    tagged_pos = pos_cache[original_sent]

    words_by_masking_strategies = [token for (token, pos, lemma) in tagged_pos if is_object(token, pos, lemma)]

    words_by_masking_strategies = filter_unreachable_words(tokenizer, tokens, words_by_masking_strategies)

    if len(words_by_masking_strategies) == 0:
        content_tokens = [token for token, pos, lemma in tagged_pos if
                         is_content_word(token, pos, lemma)]
        words_by_masking_strategies = content_tokens
        words_by_masking_strategies = filter_unreachable_words(tokenizer, tokens,
                                                               words_by_masking_strategies)
    if len(words_by_masking_strategies) > 0:
        chosen_word_to_mask = random.choice(words_by_masking_strategies)
        chosen_tokens_to_mask = tokenizer.tokenize(chosen_word_to_mask)
    else:
        chosen_tokens_to_mask = []
    output_label = []

    iterate_and_mask(chosen_tokens_to_mask, output_label, tokenizer, tokens)

    return tokens, output_label


def random_word_content_words_high(tokens, tokenizer, original_sent, pos_cache):
    """
    Masking strategy: Content words high. Mask 1 word, 80% content words, 20% stop-word or punctuation.
    :param tokens: same argument as original random_word function.
    :param tokenizer: the BertTokenizer used for the original implementation.
    :param original_sent: The sentence.
    :param pos_cache: A cache to hold the word, pos tag, lemma
    :return: (list of str, list of int), masked tokens and related labels for LM prediction
    """
    prob_dist = {'cw': 0.8, 'sw': 0.2}

    tagged_pos = pos_cache[original_sent]

    content_words = [word for word, pos, lemma in tagged_pos if
                      is_content_word(word, pos, lemma)]
    content_words = filter_unreachable_words(tokenizer, tokens, content_words)
    stop_words = [word for word, pos, lemma in tagged_pos if
                      not is_content_word(word, pos, lemma)]
    stop_words = filter_unreachable_words(tokenizer, tokens, stop_words)

    if random.random() < prob_dist['cw'] and len(content_words) > 0:
        words_by_masking_strategies = content_words
    elif len(stop_words) > 0:
        words_by_masking_strategies = stop_words
    else:
        words_by_masking_strategies = content_words

    chosen_word_to_mask = random.choice(words_by_masking_strategies)
    chosen_tokens_to_mask = tokenizer.tokenize(chosen_word_to_mask)

    output_label = []

    iterate_and_mask(chosen_tokens_to_mask, output_label, tokenizer, tokens)

    return tokens, output_label


def random_word_top_concrete(tokens, tokenizer, original_sent, pos_cache_concrete, max_seq_length):
    """
    Masking strategy: Top Concrete
    :param tokens: same argument as original random_word function.
    :param tokenizer: the BertTokenizer used for the original implementation.
    :param original_sent: The sentence.
    :param max_seq_length: Maximum sequence length of the model (20 in the original implementation).
    :param pos_cache_concrete: A cache to hold the word, pos tag, lemma, and concreteness annotated value
    :return: (list of str, list of int), masked tokens and related labels for LM prediction
    """
    if original_sent in pos_cache_concrete:
        tagged_pos = pos_cache_concrete[original_sent]
        tagged_pos = [{'word': x[0], 'pos': x[1], 'lemma': x[2], 'concreteness': x[3]} for x in tagged_pos]
    else:
        print(f'Sent not in cache: {original_sent}')
        raise Exception(f'Sent not in cache: {original_sent}')
    for x in tagged_pos:
        x_tokens = tokenizer.tokenize(x['word'])
        x['tokens'] = x_tokens

    changed_tokens = False
    changed_tokens, tokens = change_tokens_if_necessary(changed_tokens, max_seq_length, tokens, tagged_pos)

    all_concrete_values_and_words = [(x['concreteness'], x['word']) for x in tagged_pos if x['word'] not in stopwords_and_punctuations]
    top_3_concrete = heapq.nlargest(3, all_concrete_values_and_words)

    if len(top_3_concrete) == 0:
        chosen_word_to_mask = random.choice([x['word'] for x in tagged_pos])
    else:
        if len(top_3_concrete) == 1:
            chosen_conc_word_to_mask = top_3_concrete[0]
        elif len(top_3_concrete) == 2:
            chosen_conc_word_to_mask = random.choices(top_3_concrete, weights=[0.75, 0.25], k=1)[0]
        else:
            chosen_conc_word_to_mask = random.choices(top_3_concrete, weights=[0.55, 0.30, 0.15], k=1)[0]
        chosen_word_to_mask_concreteness, chosen_word_to_mask = chosen_conc_word_to_mask[0], chosen_conc_word_to_mask[1]

    chosen_tokens_to_mask = tokenizer.tokenize(chosen_word_to_mask)

    output_label = []

    iterate_and_mask(chosen_tokens_to_mask, output_label, tokenizer, tokens)

    return tokens, output_label



def iterate_and_mask(chosen_tokens_to_mask, output_label, tokenizer, tokens):
    for i, token in enumerate(tokens):
        if token in chosen_tokens_to_mask:
            random_num = random.random()

            # 80% randomly change token to mask token
            if random_num < 0.8:
                tokens[i] = "[MASK]"

            # 10% randomly change token to random token
            elif random_num < 0.9:
                tokens[i] = random.choice(list(tokenizer.vocab.items()))[0]

            # -> rest 10% randomly keep current token

            # append current token to output (we will predict these later)
            try:
                output_label.append(tokenizer.vocab[token])
            except KeyError:
                # For unknown words (should not occur with BPE vocab)
                output_label.append(tokenizer.vocab["[UNK]"])
        else:
            # no masking token (will be ignored by loss function later)
            output_label.append(-1)


def change_tokens_if_necessary(changed_tokens, max_seq_length, tokens, tagged_pos):
    inferred_pos = []
    for t in tagged_pos:
        tokenized_tokens = t['tokens']
        tokenized_tokens_with_pos = [{'token': x, 'pos': t['pos'], 'lemma': t['lemma'], 'word': t['word']} for x in tokenized_tokens]
        inferred_pos += tokenized_tokens_with_pos
    inferred_pos = inferred_pos[: (max_seq_length - 2)]
    if [x['token'] for x in inferred_pos] != tokens:
        tokens = [x['token'] for x in inferred_pos]
        changed_tokens = True
    return changed_tokens, tokens


def filter_unreachable_words(tokenizer, tokens, words_by_masking_strategies):
    tokenized_words_by_masking_strategies = [tokenizer.tokenize(w) for w in words_by_masking_strategies]

    words_by_masking_strategies_filtered_unreachable = []
    tokenized_words_by_masking_strategies_filtered_unreachable = []
    assert len(words_by_masking_strategies) == len(tokenized_words_by_masking_strategies)
    for w, w_tokenized_lst in zip(words_by_masking_strategies, tokenized_words_by_masking_strategies):
        if all(x in tokens for x in w_tokenized_lst):
            words_by_masking_strategies_filtered_unreachable.append(w)
            tokenized_words_by_masking_strategies_filtered_unreachable += w_tokenized_lst

    if len(words_by_masking_strategies) != len(words_by_masking_strategies_filtered_unreachable):
        assert all(xi in tokens for xi in tokenized_words_by_masking_strategies_filtered_unreachable)

    return words_by_masking_strategies_filtered_unreachable