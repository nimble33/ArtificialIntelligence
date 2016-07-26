footpath(52,53).
footpath(52,54).
footpath(52,57).
footpath(52,59).
footpath(52,60).
footpath(52,62).
footpath(52,68).
footpath(52,83).


footpath(53,54).
motorway(53,54).
motorway(53,60).
motorway(53,68).
motorway(53,83).

motorway(54,56).
motorway(54,60).
motorway(54,68).
motorway(54,83).

footpath(56,57).
footpath(56,58).

footpath(57,54).
footpath(57,53).
footpath(57,62).
footpath(57,58).
footpath(57,59).

footpath(58,59).

footpath(59,60).

motorway(60,68).
motorway(60,83).
motorway(60,68).
motorway(60,62).

motorway(62,83).
motorway(62,63).
motorway(62,64).
motorway(62,76).
motorway(62,66).

motorway(63,64).
motorway(63,76).
motorway(63,66).
motorway(63,68).
motorway(63,69).

motorway(64,69).
motorway(64,76).
motorway(64,66).
motorway(64,68).

footpath(65,68).
footpath(65,83).

motorway(66,69).
motorway(66,76).

footpath(69,76).



/*route(X, Y) :- footpath(X, Y); motorway(X, Y).*/
route(X,Y):-
findall(Intermediate, get_intermediate(X,Y,Intermediate), Intermediates),
    write(Intermediates).
get_intermediate(Start, End, []) :- 
    footpath(Start, End);motorway(Start,End).
 get_intermediate(Start, End, [Intermediate|Result]) :-
    footpath(Start, Intermediate);motorway(Start,End),
    /*recursion*/
    get_intermediate(Intermediate, End, Result).   

