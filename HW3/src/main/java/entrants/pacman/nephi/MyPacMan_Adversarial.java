package entrants.pacman.nephi;
import pacman.controllers.PacmanController;
import pacman.controllers.examples.StarterGhosts;
import pacman.game.Constants.MOVE;
import pacman.game.Game;

public class MyPacMan_Adversarial extends PacmanController {
	private int MAX_DEPTH=6;
	public static StarterGhosts ghosts = new StarterGhosts();

	public MOVE getMove(Game game, long timeDue) {

		int bestScore = Integer.MIN_VALUE;
		MOVE bestMove=MOVE.NEUTRAL;

		for (MOVE m : game.getPossibleMoves(game.getPacmanCurrentNodeIndex())) {
			Game gc = game.copy();

			gc.advanceGame(m, ghosts.getMove(game, -1));

			int tempScore = alphaBetaPruning(gc, MAX_DEPTH,Integer.MIN_VALUE,Integer.MAX_VALUE, false);
			if (bestScore < tempScore) {
				bestScore = tempScore;
				bestMove = m;
			}


		}
		//System.out.println("Best Score:" + bestScore); 
		//System.out.println( "Move:"+ bestMove);
		return bestMove;
	}

	public int alphaBetaPruning(Game gc,int maxdepth, int alpha, int beta, boolean max) {
		// Terminal Node case
		if (maxdepth < 1) return Evaluate(gc);
		// Maximizer
		if (max) {
			int highscore = Integer.MIN_VALUE;
			for (MOVE m :  gc.getPossibleMoves(gc.getPacmanCurrentNodeIndex())) {
				Game gameCopy = gc.copy();
				gameCopy.advanceGame(m, ghosts.getMove(gameCopy, -1));
				int temp = alphaBetaPruning(gc, maxdepth - 1,alpha,beta, false);
				highscore = Math.max(highscore, temp);
				alpha = Math.max(alpha,highscore);
				if(beta <= alpha){
					break;
				}
			}

			return highscore;
		}
		//Minimizer
		else {
			int highscore = Integer.MAX_VALUE;
			for (MOVE m :  gc.getPossibleMoves(gc.getPacmanCurrentNodeIndex())) {
				Game gameCopy = gc.copy();
				gameCopy.advanceGame(m, ghosts.getMove(gameCopy, -1));				
				int temp = alphaBetaPruning(gc, maxdepth - 1,alpha,beta, true);
				highscore = Math.min(highscore, temp);
				beta = Math.min(beta,highscore);
				if(beta <= alpha){
					break;
				}
			}
			return highscore;
		}
	}
	private int Evaluate(Game gameState) {

		int score = 0;
		if ( gameState.wasPacManEaten() ) {
			score = Integer.MIN_VALUE;
		}
		//Capture distances between pacman and ghosts

		//Capture pill data (Available, distance)


		return score;
	}

}