"""
    This file is part of reserbot.

    reserbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    reserbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with reserbot.  If not, see <http://www.gnu.org/licenses/>.

    Copyright 2010, 2011, 2012 by neuromancer, albatross
"""

import random

import src.io.categories.Categories as Categories
import src.core.Mind as Mind
import src.Stats as Stats
from src.aux import load_words_from_text

# generation of data (code contributed by albatross)

bools = ["True","False", "not False", "not True"] 
ops = ["and", "or"]

def dfs(depth, expr):
    if depth == 0:
        yield expr, eval(' '.join(expr))
    elif depth % 2 == 1:
        for b in bools:
            for x in dfs(depth - 1, expr + [b]):
                yield x
    else:
        for o in ops:
            for x in dfs(depth - 1, expr + [o]):
                yield x

trues  = []
falses = []
                
for d in range(1, 12, 2):
    for X, y in dfs(d, []):
        if (y):
            trues.append(X)
        else:
            falses.append(X)
            
print "Number of true formulas", len(trues)
print "Number of false formulas", len(falses)

train_len = 8000
test_len  = 300

true_sample = random.sample(trues, train_len+test_len)
true_train_sample = true_sample[0:train_len]
true_test_sample = true_sample[train_len : (train_len+test_len)]

false_sample = random.sample(falses, train_len+test_len)
false_train_sample = false_sample[0:train_len]
false_test_sample = false_sample[train_len : (train_len+test_len)]

# mind initilization

binput  = Categories.InputCats(bools+ops, "Logic")
boutput = Categories.OutputCats(bools[0:2], "Logic")

mind = Mind.Mind([binput], [boutput], [])

# mind training

print "Assimilating true exps.."
bool_inputs = dict( SeqCatLogic = ["True"])

for e in true_train_sample:
    formula_inputs = dict( SeqCatLogic = e)
    mind.assimilate(formula_inputs)
    mind.assimilate(bool_inputs)
    mind.stop()

print "Assimilating false exps.."
bool_inputs = dict( SeqCatLogic = ["False"])

for e in false_train_sample:
    formula_inputs = dict( SeqCatLogic = e)
    mind.assimilate(formula_inputs)
    mind.assimilate(bool_inputs)
    mind.stop()

# mind flushing trains several regression models to predict future data
    
mind.stop(flush = True)

# mind stats computes error

stats = Stats.Stats(mind)

# mind testing

for e in true_test_sample:
     formula_inputs = dict( SeqCatLogic = e)
     stats.evalSample(formula_inputs, "True", False)


for e in false_test_sample:
     formula_inputs = dict( SeqCatLogic = e)
     stats.evalSample(formula_inputs, "False", False)

print "Test error -> ", stats.getError()

# TODO: Move to TUI.py

#while True:
#    print ">",
#    try:
#        words = raw_input()
#    except EOFError:
#        break
#    word_inputs = dict( InputWordsEn = words)
#    print mind.assimilate(word_inputs)
#    mind.stop()

