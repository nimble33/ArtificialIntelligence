package entrants.pacman.nephi;
import pacman.controllers.PacmanController;
import pacman.controllers.examples.StarterGhosts;
import pacman.game.Constants.DM;
import pacman.game.Constants.GHOST;
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

			int tempScore = alphaBetaPruning(gc, MAX_DEPTH,Integer.MIN_VALUE,Integer.MAX_VALUE, true);
			if (bestScore < tempScore) {
				bestScore = tempScore;
				bestMove = m;
			}


		}
		return bestMove;
	}

/*
 * Algorithm Source:
 * https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
 */
	
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
					break; //Beta cutoff
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
					break; //Alpha cutoff
				}
			}
			return highscore;
		}
	}

	public static int Evaluate(Game gameState) {
		//Reset
		if (gameState.wasPacManEaten()) {
			return Integer.MIN_VALUE;
		}
		int currentIndex = gameState.getPacmanCurrentNodeIndex();

		int ghostScore = 0;
		//Capture distances between pacman and ghosts
		for (GHOST ghost : GHOST.values()) {
			int ghostIndex=gameState.getGhostCurrentNodeIndex(ghost);
			int distance = gameState.getShortestPathDistance(currentIndex,ghostIndex);
			//If ghost Edible +ve Multiplier
			if(gameState.isGhostEdible(ghost)){
				ghostScore +=(30 / distance);
			}
			//Ghost not Edible -ve Multiplier
			else{
				ghostScore += -1 *(30 / distance);	
			}

		}

		//Capture pill data (Available, distance)
		int[] aPI = gameState.getActivePillsIndices();
		int[] aPPI = gameState.getActivePowerPillsIndices();
		int[] allActivePillIndices = merge(aPI,aPPI);
		int pillDistance =  gameState.getShortestPathDistance(currentIndex,gameState.getClosestNodeIndexFromNodeIndex(currentIndex, allActivePillIndices, DM.PATH));


		//Heuristic
		return ghostScore + gameState.getScore() * 100 - pillDistance;
	}

	private static int[] merge(int[] aPI, int[] aPPI) {
		int length = aPI.length + aPPI.length;
		int[] result = new int[length];
		System.arraycopy(aPI, 0, result, 0, aPI.length);
		System.arraycopy(aPPI, 0, result, aPI.length, aPPI.length);	 
		return result;
	}


}