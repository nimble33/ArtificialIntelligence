package entrants.pacman.nephi;

import pacman.controllers.PacmanController;
import pacman.game.Constants.*;
import pacman.game.Game;
import pacman.game.internal.Node;
import pacman.game.Constants;
import java.util.Stack;

/*
 * PacMan Search based on DFS: Works for Partially Observable Environment - Uninformed Search
 * Search Applies only to PacMan - Ghosts are Neglected
 * 
 * 1. Initialize Stack
 * 2. Push Start Node into Stack
 * 3. Mark Start Node as Visited
 * loop
 * 4. Get Top
 * 5. Get Children of Top
 * 6. If Child Node Unvisited 
 * 7. Mark Unvisited child as visited
 * 8. Push Unvisited child onto Stack
 * 9. If no child nodes - Retract Move
 * end loop
 * 
 */
public class MyPacMan_DFS extends PacmanController {
	private Stack<Node> dfsStack=new Stack<Node>(); //Stack to maintain nodes
	private boolean isPlaying= false; //game state
	private MOVE myMove;
	private boolean visited[]; //visited? NodeArray
	public MOVE getMove(Game game, long timeDue) {

		//Playing Mode
		if(isPlaying!=true ||  game.wasPacManEaten()){
			int current = game.getPacmanCurrentNodeIndex(); //Current Pacman index
			Node[] dfsGraph= game.getCurrentMaze().graph; // current maze graph - set of nodes
			Node currentPacManNode= dfsGraph[current]; //current node in the graph
			dfsStack.push(currentPacManNode); // add current Node
			visited=new boolean[dfsGraph.length];//initialize to maze length
			visited[currentPacManNode.nodeIndex]=true; //Mark root as visited 
			isPlaying=true;   		
		}

		Node top=dfsStack.peek(); // Retrieve Top Node 

		int unvisitedTargetNodeIndex=selectFromNeighborsUnvisited(top,game); 
		if(unvisitedTargetNodeIndex!=0){
			visited[unvisitedTargetNodeIndex]=true; // Mark Target as Visited
			Node entry=game.getCurrentMaze().graph[unvisitedTargetNodeIndex]; //Get Node at that particular Index
			dfsStack.push(entry);// Push the entry
			//Update Move towards Target(Selected Via DFS)
			myMove= game.getNextMoveTowardsTarget(game.getPacmanCurrentNodeIndex(), unvisitedTargetNodeIndex, DM.PATH);  
		} 
		//Null Values - Retract
		else{
			dfsStack.pop();
			Node newTop=dfsStack.peek();
			myMove= game.getNextMoveTowardsTarget(top.nodeIndex, newTop.nodeIndex, Constants.DM.PATH);

		}

		return myMove;
	}

	//Returns Target Node Index if it is Unvisited 
	private int selectFromNeighborsUnvisited(Node top, Game game) {

		int[] neighbours=game.getNeighbouringNodes(top.nodeIndex);
		for(int i=0;i<neighbours.length;i++){
			if (!visited[neighbours[i]]) {
				return neighbours[i];
			}
		}
		return 0;
	}
}

