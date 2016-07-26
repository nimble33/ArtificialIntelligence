package entrants.pacman.nephi;
import pacman.controllers.PacmanController;
import pacman.controllers.examples.StarterGhosts;
import pacman.game.Constants.DM;
import pacman.game.Constants.GHOST;
import pacman.game.Constants.MOVE;
import pacman.game.Game;

import java.util.ArrayList;
import java.util.EnumMap;
import java.util.List;

public class MyPacMan_Adversarial extends PacmanController {
	private int MAX_DEPTH=4;
	int bestScore = Integer.MIN_VALUE;
	MOVE bestMove=MOVE.NEUTRAL;

	public static StarterGhosts ghosts = new StarterGhosts();

	public MOVE getMove(Game game, long timeDue) {

		//Stores every ghost's current move
		EnumMap<GHOST, MOVE> ghostMoves = new EnumMap<GHOST, MOVE>(GHOST.class);
		//All Possible moves for PacMan(up,down,left,right)
		List<MOVE> possibleMoves=new ArrayList<>();
		populateCollections(game,ghostMoves,possibleMoves);		
		int leftMoveHeuristic = 0, rightMoveHeuristic = 0, topMoveHeuristic = 0, downMoveHeuristic = 0;

		//Retrieve values for a PacMan Move and Ghost Move
		for (int i = 0; i < possibleMoves.size(); i++) {			
			Game copy = game.copy();
			switch(possibleMoves.get(i)) {
			case LEFT:
				copy.advanceGame(MOVE.LEFT, ghostMoves);
				leftMoveHeuristic = alphaBetaPruning(copy, ghostMoves,MAX_DEPTH-1,Integer.MIN_VALUE, Integer.MAX_VALUE,false);
				break;
			case RIGHT:
				copy.advanceGame(MOVE.RIGHT, ghostMoves);
				rightMoveHeuristic =  alphaBetaPruning(copy, ghostMoves,MAX_DEPTH-1,Integer.MIN_VALUE, Integer.MAX_VALUE,false);
				break;
			case UP:
				copy.advanceGame(MOVE.UP, ghostMoves);
				topMoveHeuristic =  alphaBetaPruning(copy, ghostMoves,MAX_DEPTH-1,Integer.MIN_VALUE, Integer.MAX_VALUE,false);
				break;
			case DOWN:
				copy.advanceGame(MOVE.DOWN, ghostMoves);
				downMoveHeuristic =  alphaBetaPruning(copy, ghostMoves,MAX_DEPTH-1,Integer.MIN_VALUE, Integer.MAX_VALUE,false);
				break;
			default:
				break;
			}
		}

		//Choose the best move among all moves based on the heuristic calculated from Alphabeta Minimax Algorithm
		return chooseBestMove(leftMoveHeuristic, rightMoveHeuristic,topMoveHeuristic,downMoveHeuristic);

	}


	//Populate the containers -EnumMap -Ghost Moves, ArrayList- PacMan Moves
	private void populateCollections(Game game, EnumMap<GHOST, MOVE> ghostMoves, List<MOVE> possibleMoves) {

		ghostMoves.put(GHOST.BLINKY, game.getGhostLastMoveMade(GHOST.BLINKY));
		ghostMoves.put(GHOST.INKY, game.getGhostLastMoveMade(GHOST.INKY));
		ghostMoves.put(GHOST.PINKY, game.getGhostLastMoveMade(GHOST.PINKY));
		ghostMoves.put(GHOST.SUE, game.getGhostLastMoveMade(GHOST.SUE));
		possibleMoves.add(MOVE.UP);
		possibleMoves.add(MOVE.DOWN);
		possibleMoves.add(MOVE.LEFT);
		possibleMoves.add(MOVE.RIGHT);

	}

	/*
	 * Algorithm Source:
	 * https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
	 */
	private int alphaBetaPruning(Game game, EnumMap<GHOST, MOVE> ghostMoves, int maxdepth, int alpha, int beta, boolean max) {
		// Terminal Node case
		if (maxdepth < 1) return evaluate(game);
		if (max) { //Maximizing Player-PacMan
			int highscore = Integer.MIN_VALUE;
			int temp =alphaBetaPruning(game, ghostMoves, maxdepth-1,alpha, beta, false);
			highscore = Math.max(highscore, temp);
			alpha = Math.max(alpha,highscore);
			if(beta <= alpha){
				return alpha; //Beta cutoff
			}
			return highscore;
		}
		else { // MinimizingPlayer-Ghosts
			int highscore = Integer.MAX_VALUE;
			int temp =alphaBetaPruning (game, ghostMoves, maxdepth-1,alpha, beta, true);
			highscore = Math.min(highscore, temp);
			beta = Math.min(beta,highscore);
			if(beta <= alpha){
				return beta; //Alpha cutoff
			}
			return highscore;
		}

	}

	//Retrieves the move with best heuristic
	private MOVE chooseBestMove(int left, int right, int top, int down)  {
		MOVE bestMove = MOVE.NEUTRAL;
		int bestScore = Integer.MIN_VALUE;
		if (left!= Integer.MIN_VALUE && left > bestScore) {
			bestMove = MOVE.LEFT;
			bestScore = left;
		}
		if (right!= Integer.MIN_VALUE && right > bestScore) {
			bestMove = MOVE.RIGHT;
			bestScore = right;
		}
		if (top!= Integer.MIN_VALUE && top > bestScore) {
			bestMove = MOVE.UP;
			bestScore = top;
		}
		if (down!= Integer.MIN_VALUE && down > bestScore) {
			bestMove = MOVE.DOWN;
			bestScore = down;
		}
		return bestMove;

	}



	// Heuristic calculation 
	// Scenarios:
	//1. Ghost Distance from PacMan
	//2. Ghost Edible - +ve Multiplier
	//3. Ghost not edible- -ve Multiplier
	//4. Pill Distance from PacMan
	public static int evaluate(Game gameState) {
		//Reset
		if (gameState.wasPacManEaten()) {
			return Integer.MIN_VALUE;
		}
		int currentIndex = gameState.getPacmanCurrentNodeIndex();

		int ghostScore = 0;
		//Capture distances between PacMan and ghosts
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

	//Function Merges two Integer arrays
	private static int[] merge(int[] aPI, int[] aPPI) {
		int length = aPI.length + aPPI.length;
		int[] result = new int[length];
		System.arraycopy(aPI, 0, result, 0, aPI.length);
		System.arraycopy(aPPI, 0, result, aPI.length, aPPI.length);	 
		return result;
	}


}