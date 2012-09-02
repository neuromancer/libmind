

shuf adjectives/28K\ adjectives.txt             | head -n $1  > adjectives.txt
shuf adverbs/6K\ adverbs.txt                    | head -n $1  > adverbs.txt
# proper nouns are filtered
cat nouns/91K\ nouns.txt | grep -v [A-Z] | shuf | head -n $1  > nouns.txt
shuf verbs/31K\ verbs.txt                       | head -n $1  > verbs.txt


D=$(echo "$1/2" | bc)

#echo $d

cat adjectives.txt | head -n $D > adjectives_train.txt
cat adjectives.txt | tail -n $D > adjectives_test.txt

cat adverbs.txt    | head -n $D > adverbs_train.txt
cat adverbs.txt    | tail -n $D > adverbs_test.txt

cat nouns.txt      | head -n $D > nouns_train.txt
cat nouns.txt      | tail -n $D > nouns_test.txt

cat verbs.txt      | head -n $D > verbs_train.txt
cat verbs.txt      | tail -n $D > verbs_test.txt
