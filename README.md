libmind
=======

A general purpose library to process and predict sequences of elements (for example, sequences 
of letters as words, or phrases) using echo state networks. The usage of libmind tries to be as simple 
as it is possible.

## Dedication
This project is dedicated to someone special who taught me the difference between hope and 
despair.

## Required dependencies for libmind:

* Python 2.7
* Oger                           (http://reservoir-computing.org/oger) 
  and this package requires:
     - Numpy 1.1 or higher       (http://numpy.scipy.org/)   
     - Scipy 0.7 or higher       (http://www.scipy.org/)
     - MDP 2.5 or higher         (http://mdp-toolkit.sourceforge.net/)

## Installation

* In Debian/Ubuntu

1. Install the dependencies of Oger:


    apt-get install python-numpy python-mdp 


2. Install Oger (a debian package generated using checkinstall is available)


    wget "https://github.com/downloads/neuromancer/libmind/oger_1.1.3-1_all.deb"
    dpkg -i oger_1.1.3-1_all.deb


* In Arch Linux

1. Install Oger from aur (http://aur.archlinux.org/packages.php?ID=51256), for example, using packer:

    packer -S python2-oger


After that, just clone this repository, and execute:

    make

to compile the C code. 
Then you are ready to start playing with libmind. 


## Using libmind

To create a simulated mind, it will be necessary to define how to vectorize its inputs' and outputs' elements. 
Once the mind is created, the initialization will bootstrap it to allow it to learn how generate
correctly its outputs' elements. An assimilation function is used to introduce inputs, one by one, in a 
sequence. Every time an input is assimilated, the prediction of the next output is returned. 
A stop function is used to finish with the current sequence, resetting the internal state of 
the simulated mind.

## Examples

The use of libmind is shown using several example or tests. The examples available are:

### Identification of part of speech (POS) of English words only using their letters

- File:      test_POS.py
- Objective: To classify isolated words into nouns, verbs, adjectives or adverbs given their letters.
- Dataset: Some words are randomly selected from this dataset: 
           http://www.ashley-bovan.co.uk/words/partsofspeech.html 
           

### Reduction of variableless propositional logic formulas

- File:      test_logic.py
- Objective: To classify between true and false variableless propositional formulas. 
- Dataset:   The dataset is generated using the following grammar:

        Formula := Formula and Formula | Formula or Formula | True | False | ~True | ~False

 The evaluation of the resulting formula is made using Python evaluation of booleans 
 (where evaluation of "and" precedes "or") 


I'm thinking in more examples to extend and improve libmind but of course, *this experimental project is 
open to new ideas!*
