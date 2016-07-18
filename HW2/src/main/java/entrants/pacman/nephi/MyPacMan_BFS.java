package entrants.pacman.nephi;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Map.Entry;

import pacman.controllers.PacmanController;
import pacman.game.Constants.MOVE;
import pacman.game.internal.Node;
import pacman.game.Game;

/*
 * BFS Implementation
 */

public class MyPacMan_BFS extends PacmanController {
 
    
	private boolean isPlaying= false; //game state
	private MOVE myMove;
	private boolean visited[]; //visited nodes?
	private Queue<Node> bfsQueue=new LinkedList<Node>(); //Queue to maintain nodes

    public MOVE getMove(Game game, long timeDue) {
    	int size = 0;
    	Node[] bfsGraph;
        //Place your game logic here to play the game as Ms Pac-Man
    	if(isPlaying!=true ||  game.wasPacManEaten()){
			int current = game.getPacmanCurrentNodeIndex(); //Current Pacman index
			 bfsGraph= game.getCurrentMaze().graph; // current maze graph - set of nodes
			Node currentPacManNode= bfsGraph[current]; //current node in the graph
			bfsQueue.add(currentPacManNode); // root node
			size=bfsGraph.length;
			visited=new boolean[size];//initialize to maze length
			visited[currentPacManNode.nodeIndex]=true; 
			isPlaying=true;   		
		}
    
    		Node n=bfsQueue.remove();    		
    		Entry<MOVE, Integer> selectedNode;    		
    		while((selectedNode = selectFromNeighbors(n))!= null)	{
    			visited[selectedNode.getValue()]=true;
    			Node entry=game.getCurrentMaze().graph[selectedNode.getValue()];
    			bfsQueue.add(entry);
    			//System.out.println(selectedNode.getKey());
    			myMove = selectedNode.getKey();    					
    		}
    		clearNodes(size,game);
    	return myMove;
    }

	private void clearNodes(int size, Game game) {
		int i=0;
		while(i<size)
		{
			Node n= game.getCurrentMaze().graph[i];
			visited[n.nodeIndex]=false;
			i++;
		}
	}

	private Entry<MOVE, Integer> selectFromNeighbors(Node n) {
		// TODO Auto-generated method stub
		for (Entry<MOVE, Integer> neighbour: n.neighbourhood.entrySet()) {
			if (!visited[neighbour.getValue()]) {
				return neighbour;
			}
		}
		return null;
	}
}

