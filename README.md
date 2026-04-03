# tictactoeMENACE

I am about 0% sure that this is optimal, but I am quite sure that it can play tic tac toe optimally 95% of the time. I would say that I can at the very least win or tie every single game and I have not been able to win a single time against it. Somehow in the training graph it shows that it loses when playing against a random opponent, which may be because the random opponent plays moves it has not seen before, and more training would do it good. Nontheless, while playing against it I have yet to win so I would say it works quite well.

Note that this is in fact a modified version of MENACE compared to what we did in class. I made two major changes. 1, instead of doing a 1 2 4 8 structure of beads, I did more like 3 9 27 81. This is not explictly defined, and is instead because I want the program to not miss any game state, and as a result only when a scenario loses that the series of steps is removed, and the 3 9 27 81 allows us to do this. 2, I made wins and ties equal in weight, and this is for two reasons. One, when playing against an optimal player, this allows it to all always tie which is optimal. Also, since the training loop was playing against itself, it did not make too much sense to give a win, which is also a loss for itself but on different turns, double the reinforcement. And additionally this allowed me to make sure that all game states were reached, by not adding beads. 

If you want to run and test it yourself, simply run the tictactoe.py file once, then run the playtictactoe.py file to play against it.

 

Gemini Chat: https://gemini.google.com/share/1819305d91a9