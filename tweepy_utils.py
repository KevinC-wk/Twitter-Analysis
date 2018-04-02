import string


# Gets the text, sans links, hashtags, mentions, media, and symbols.
def get_text_cleaned(tweet):
    text = tweet['text']

    slices = []
    # Strip out the urls.
    if 'urls' in tweet['entities']:
        for url in tweet['entities']['urls']:
            slices += [{'start': url['indices'][0], 'stop': url['indices'][1]}]

    # Strip out the hashtags.
    if 'hashtags' in tweet['entities']:
        for tag in tweet['entities']['hashtags']:
            slices += [{'start': tag['indices'][0], 'stop': tag['indices'][1]}]

    # Strip out the user mentions.
    if 'user_mentions' in tweet['entities']:
        for men in tweet['entities']['user_mentions']:
            slices += [{'start': men['indices'][0], 'stop': men['indices'][1]}]

    # Strip out the media.
    if 'media' in tweet['entities']:
        for med in tweet['entities']['media']:
            slices += [{'start': med['indices'][0], 'stop': med['indices'][1]}]

    # Strip out the symbols.
    if 'symbols' in tweet['entities']:
        for sym in tweet['entities']['symbols']:
            slices += [{'start': sym['indices'][0], 'stop': sym['indices'][1]}]

    # Sort the slices from highest start to lowest.
    slices = sorted(slices, key=lambda x: -x['start'])

    # No offsets, since we're sorted from highest to lowest.
    for s in slices:
        text = text[:s['start']] + text[s['stop']:]

    return text


# Sanitizes the text by removing front and end punctuation,
# making words lower case, and removing any empty strings.
def get_text_sanitized(tweet):
    return ' '.join([w.lower().strip().rstrip(string.punctuation)
                    .lstrip(string.punctuation).strip()
                     for w in get_text_cleaned(tweet).split()
                     if w.strip().rstrip(string.punctuation).strip()])
