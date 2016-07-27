/*predicates wife, son and daughter. */

wife(elizabeth,philip).
son(charles,philip).
son(charles,elizabeth).
daughter(anne,philip).
daughter(anne,elizabeth).
son(andrew,philip).
son(andrew,elizabeth).
son(edward,philip).
son(edward,elizabeth).

wife(diana,charles).
son(william,charles).
son(william,diana).
son(harry,charles).
son(harry,diana).

wife(camilla,charles).

wife(anne,markphilips).
son(peter,markphilips).
son(peter,anne).
daughter(zara,markphilips).
daughter(zara,anne).

wife(anne,timothy).


wife(sarah,andrew).
daughter(beatrice,andrew).
daughter(beatrice,sarah).
daughter(eugenie,andrew).
daughter(eugenie,sarah).

wife(sophie,edward).
daughter(louise,edward).
daughter(louise,sophie).
son(james,edward).
son(james,sophie).

wife(kate,william).
son(george,william).
son(george,kate).

wife(autumn,peter).
daughter(savannah,peter).
daughter(savannah,autumn).
daughter(isla,peter).
daughter(isla,autumn).

wife(zara,mike).
daughter(mia,mike).
daughter(mia,zara).

/*Rules*/

husband(X,Y):- wife(Y,X).
spouse(X,Y):- wife(X,Y);husband(X,Y).
child(X,Y):-son(X,Y);daughter(X,Y).
parent(X,Y):-child(Y,X).
grandParent(X,Y):-parent(P,Y),parent(X,P).
grandChild(X,Y):-grandParent(Y,X).
greatGrandParent(X,Y):-parent(P,Y),grandParent(X,P).
greatGrandChild(X,Y):-greatGrandParent(Y,X).
brother(X,Y):- son(X,Z),child(Y,Z),X\=Y.
sister(X,Y):- daughter(X,Z),child(Y,Z),X\=Y.
uncle(X,Y):- parent(Z,Y),brother(X,Z);aunt(Z,Y),husband(X,Z).
aunt(X,Y):- parent(Z,Y),sister(X,Z);uncle(Z,Y),wife(X,Z). 
brotherInLaw(X,Y):-spouse(Z,Y),brother(X,Z).
sisterInLaw(X,Y):- spouse(Z,Y),sister(X,Z).
brotherSisterInLaw(X,Y):- brotherInLaw(X,Y);sisterInLaw(X,Y).
niece(X,Y):- daughter(X,Z),wife(Z,W),brother(W,Y);daughter(X,Z),sister(Z,Y).


    
