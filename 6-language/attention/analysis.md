# Analysis

## Layer 1, Head 11

- Attempting to interpret the way the model pays attention to the relationship between a noun and the adjective(s) that describe it
- In this case we are masking the expected adjective
- For the first example sentence, for the masked word, this attention head pays closest attention to the word 'roses'
- For the second example sentence, this attention head pays closest attention to "tree" for the masked word
- This indicates that in order predict the masked word (which in this case would likely be some descriptor) of the following noun, this attention head pays closest attention to the noun

Example Sentences:
- The gardener watered the [MASK] roses in the backyard.
- They sat under a [MASK] tree during the summer heat.

## Layer 2, Head 7

- Attempting to interpret the way the model pays attention to the relationship between a noun and the adjective(s) that describe it
- In this case we are masking the noun
- For the first example sentence, this attention head pays significant attention to [MASK], for both the 'ripe' and 'juicy' adjectives
- For the second example, this behaviour is repeated. This attention head pays closest attention to [MASK] for the adjectives 'vibrant' and 'colorful'
- This indicates that this attention head is in some way assessing the link between adjectives prior to the masked word in order to predict the masked word

Example Sentences:
- He placed the ripe, juicy [MASK] on the counter.
- The artist painted a vibrant, colorful [MASK] on the wall.