AR=".."
WO="${AR}/.."

#~ python ${AR}/utils/tweet-html.py \
    #~ ${WO}/.trash/twitter-2024-06-18-2c71a0cbc9c0fbf1021e2250917e3c81ed93f2c66d160b225b89c795b468aa25/data/tweets.js \
    #~ ${AR}/social/x_ai_refuge.html \
    #~ "@ai_refuge Twitter/X archive"

#~ python ${AR}/utils/tweet-html.py \
    #~ ${WO}/.trash/twitter-2024-06-19-682ded539965011649a6f5632cde364b1370b13080b2580341a79bf1fe93d99b/data/tweets.js \
    #~ ${AR}/social/x_weird_offspring.html \
    #~ "@weird_offspring Twitter/X archive"

python ${AR}/utils/tweet-html.py \
    ${WO}/.trash/x_data_2/ai-refuge-twitter-2024-07-25-2c71a0cbc9c0fbf1021e2250917e3c81ed93f2c66d160b225b89c795b468aa25/data/tweets.js \
    ${AR}/social/x_ai_refuge.html \
    "@ai_refuge Twitter/X archive"

python ${AR}/utils/tweet-html.py \
    ${WO}/.trash/x_data_2/weird_offspring-twitter-2024-07-25-682ded539965011649a6f5632cde364b1370b13080b2580341a79bf1fe93d99b/data/tweets.js \
    ${AR}/social/x_weird_offspring.html \
    "@weird_offspring Twitter/X archive"
