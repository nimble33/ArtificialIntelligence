package entrants.pacman.nephi;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;

import pacman.controllers.PacmanController;
import pacman.game.Constants.DM;
import pacman.game.Constants.MOVE;
import pacman.game.Game;


/*
 * Greedy Best First Search - Informed Search
 * Starting Lines of Code taken from Examples - POPacMan.java
 * Search Applies only to PacMan - Ghosts are Neglected
 * 
 * 1. Retrieve all Node Indices of Targets
 * 2. Initialize Visited, HashMap to store heuristics and their corresponding Node Indices
 * 3. The heuristics- Manhattan Distance are sorted in ascending order. 
 * 4. The HashMap consists of successors of current Node arranged in increasing orders
 * 5. Return the Node with the best heuristic as the targetNode
 */
public class MyPacMan_GBFS extends PacmanController {

	public MOVE getMove(Game game, long timeDue) {

		int current = game.getPacmanCurrentNodeIndex();


		// Strategy 3: Go after the pills and power pills that we can see
		int[] pills = game.getPillIndices();
		int[] powerPills = game.getPowerPillIndices();

		ArrayList<Integer> targets = new ArrayList<Integer>();

		for (int i = 0; i < pills.length; i++) {
			//check which pills are available
			Boolean pillStillAvailable = game.isPillStillAvailable(i);
			if (pillStillAvailable == null) continue;
			if (game.isPillStillAvailable(i)) {
				targets.add(pills[i]);
			}
			// System.out.println(targets.size());
		}

		for (int i = 0; i < powerPills.length; i++) {            //check with power pills are available
			Boolean pillStillAvailable = game.isPillStillAvailable(i);
			if (pillStillAvailable == null) continue;
			if (game.isPowerPillStillAvailable(i)) {
				targets.add(powerPills[i]);
			}
		}
		//    System.out.println(targets.size());
		int[] targetsArray = new int[targets.size()]; 
		if (!targets.isEmpty()) {
			//convert from ArrayList to array

			for (int i = 0; i < targetsArray.length; i++) {
				targetsArray[i] = targets.get(i);
			}
		}

		int targetNodeIndex=selectNodeGBFS(current,targetsArray,game);
		return game.getNextMoveTowardsTarget(current, targetNodeIndex, DM.PATH);         
	}
	//Works for Observable Environment
	private int selectNodeGBFS(int current, int[] targetsArray, Game game) {
		// Mark the visited Nodes
		Set<Integer> visited = new HashSet<>();
		// HashMap to store the Heuristic and Node Index
		HashMap<Integer,Integer> heuristicMap=new HashMap<Integer,Integer>();
		visited.add(current);
		// Load HashMap with corresponding heuristics(Manhattan Distance of the NodeIndex) 
		for (int i = 0; i < targetsArray.length; i++) {  
			if(!visited.contains((targetsArray[i]))){
				int heuristic = game.getManhattanDistance(current, targetsArray[i]);
				heuristicMap.put(heuristic,targetsArray[i]);
			}

		}   
		// Sort the Keys - Heuristic in increasing order
		ArrayList<Integer> sortedKeysList = new ArrayList<>(heuristicMap.keySet());
		Collections.sort(sortedKeysList);
		//Get the Node Index of the first value of the ArrayList
		int targetNode=heuristicMap.get(sortedKeysList.get(0));
		return targetNode;

	}
}