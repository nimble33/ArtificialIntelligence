package entrants.pacman.nephi;
import pacman.controllers.PacmanController;
import pacman.game.Game;
import pacman.game.Constants.MOVE;
import static pacman.game.Constants.DM;

import java.util.ArrayList;
import entrants.pacman.nephi.AStar;


// Code taken from Examples - POPacMan.java
// Astar - Applicable only to PacMan


public class MyPacMan_AStar extends PacmanController {

	private MOVE myMove;
	@Override
	public MOVE getMove(Game game, long timeDue) {

		// Should always be possible as we are PacMan
		int current = game.getPacmanCurrentNodeIndex();

		// Strategy 3: Go after the pills and power pills that we can see
		int[] pills = game.getPillIndices();
		int[] powerPills = game.getPowerPillIndices();

		ArrayList<Integer> targets = new ArrayList<Integer>();
		ArrayList<Integer> path = new ArrayList<Integer>();
		for (int i = 0; i < pills.length; i++) {
			//check which pills are available
			Boolean pillStillAvailable = game.isPillStillAvailable(i);
			if (pillStillAvailable == null) continue;
			if (game.isPillStillAvailable(i)) {
				targets.add(pills[i]);
			}
		}

		for (int i = 0; i < powerPills.length; i++) {            //check with power pills are available
			Boolean pillStillAvailable = game.isPillStillAvailable(i);
			if (pillStillAvailable == null) continue;
			if (game.isPowerPillStillAvailable(i)) {
				targets.add(powerPills[i]);
			}
		}
		int[] targetsArray = new int[targets.size()]; 
		if (!targets.isEmpty()) {
			for (int i = 0; i < targetsArray.length; i++) {
				targetsArray[i] = targets.get(i);
			}
		}
		if(game.wasPacManEaten()){
			path = new ArrayList<Integer>();
		}

		if(path.isEmpty()){
			//Choose an Index for destination
			int closestIndex = game.getClosestNodeIndexFromNodeIndex(current, targetsArray,DM.PATH);
			AStar a=new AStar();
			a.createGraph(game.getCurrentMaze().graph);
			int[] targetPath=a.computePathsAStar(current,closestIndex, game); // Retrieve Path using AStar 

			if (targetPath.length > 0) {
				for(int i = 1; i < targetPath.length; i++){
					path.add(targetPath[i]); // array to Array list
				}
			}
		}
		//moves based on the path extracted from A* path finding algorithm
		if (path.size() > 0) {
			myMove = game.getNextMoveTowardsTarget(game.getPacmanCurrentNodeIndex(), path.remove(0),DM.PATH);
		}
		else {
			myMove = MOVE.NEUTRAL;
		}
		return myMove;
	}
}







