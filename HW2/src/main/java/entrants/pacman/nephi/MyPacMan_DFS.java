package entrants.pacman.nephi;

import pacman.controllers.PacmanController;
import pacman.game.Constants.*;
import pacman.game.Game;
import pacman.game.internal.Node;
import pacman.game.Constants;
import java.util.Map.Entry;
import java.util.Stack;

/*
 * PacMan Search based on DFS
 */
public class MyPacMan_DFS extends PacmanController {
	private Stack<Node> dfsStack=new Stack<Node>(); //Stack to maintain nodes
	private boolean isPlaying= false; //game state
	private MOVE myMove;
	private boolean visited[]; //visited nodes?
	public MOVE getMove(Game game, long timeDue) {

		//Start state
		if(isPlaying!=true ||  game.wasPacManEaten()){
			int current = game.getPacmanCurrentNodeIndex(); //Current Pacman index
			Node[] dfsGraph= game.getCurrentMaze().graph; // current maze graph - set of nodes
			Node currentPacManNode= dfsGraph[current]; //current node in the graph
			dfsStack.push(currentPacManNode); // add
			visited=new boolean[dfsGraph.length];//initialize to maze length
			visited[currentPacManNode.nodeIndex]=true; //root 
			isPlaying=true;   		
		}

		Node top=dfsStack.peek();

		/*
				1. Find neighbors of top
		    	2. If neighbors not in visited, choose the one based on dfs 
		    	3. Get its node index and the move
		    	4. Mark the node as visited push it to stack 
		    	5. update the move 
		 */


		Entry<MOVE, Integer> selectedNode = selectFromNeighbors(top);

		//To visit
		if(selectedNode != null){
			visited[selectedNode.getValue()]=true;
			Node entry=game.getCurrentMaze().graph[selectedNode.getValue()];
			dfsStack.push(entry);
			myMove = selectedNode.getKey();
		}
		//Null Handler
		else{
			myMove= game.getNextMoveTowardsTarget(top.nodeIndex, dfsStack.pop().nodeIndex, Constants.DM.PATH);
			
		}
		return myMove;
	}

	private Entry<MOVE, Integer> selectFromNeighbors(Node top) {
		for (Entry<MOVE, Integer> neighbour: top.neighbourhood.entrySet()) {
			if (!visited[neighbour.getValue()]) {
				return neighbour;
			}
		}
		return null;
	}
}

