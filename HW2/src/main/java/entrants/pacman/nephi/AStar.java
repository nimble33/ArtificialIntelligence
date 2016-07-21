package entrants.pacman.nephi;


import pacman.game.Constants.MOVE;
import pacman.game.Game;
import pacman.game.internal.Node;


import java.util.ArrayList;
import java.util.Collections;
import java.util.EnumMap;
import java.util.PriorityQueue;


/*
 * Code Sample taken from pacman.game.internal.AStar. Heuristic Changed from Shortest path
 * distance to Manhattan Distance
 * 
 * 1. Construct the graph with new node type N(contains g,h) by passing the 
 * current maze's graph
 * 2. Initialize open
 * 3. Initialize closed
 * 4. Place start node into open
 * 5. loop - While open not empty
 * 6. poll the open list(the node with least f=g+h)
 * 7. find popped nodes children
 * 8. for each child
 * 9. if successor is the target then break
 * 10. child's gvalue=popped node's g+distance between the child and popped node
 * 11. child's fvalue=gvalue+h(heuristic measure)
 * 12. If the node same as the child is in open list with lower f->skip the node
 * 13. do as above for closed list
 * 14. else add the child to open list
 * 15. return the path to reach target  
 * 
 * 
 */
public class AStar {
	private N[] graph;

	public void createGraph(Node[] nodes) {
		graph = new N[nodes.length];

		//create graph
		for (int i = 0; i < nodes.length; i++)
			graph[i] = new N(nodes[i].nodeIndex);

		//add neighbours
		for (int i = 0; i < nodes.length; i++) {
			EnumMap<MOVE, Integer> neighbours = nodes[i].neighbourhood;
			MOVE[] moves = MOVE.values();

			for (int j = 0; j < moves.length; j++)
				if (neighbours.containsKey(moves[j]))
					graph[i].adj.add(new E(graph[neighbours.get(moves[j])], moves[j], 1));
		}
	}

	public synchronized int[] computePathsAStar(int s, int t, MOVE lastMoveMade, Game game) {

		N start = graph[s];        
		N target = graph[t];

		PriorityQueue<N> open = new PriorityQueue<N>();
		ArrayList<N> closed = new ArrayList<N>();

		start.g = 0;
		//Heuristic changed to Manhattan distance
		start.h = game.getManhattanDistance(start.index, target.index);

		start.reached = lastMoveMade;

		open.add(start);

		while (!open.isEmpty()) {
			N currentNode = open.poll();
			closed.add(currentNode);

			if (currentNode.isEqual(target))
				break;

			for (E next : currentNode.adj) {
				if (next.move != currentNode.reached.opposite()) {
					double currentDistance = next.cost;
					if (!open.contains(next.node) && !closed.contains(next.node)) {
						next.node.g = currentDistance + currentNode.g;
						next.node.h = game.getShortestPathDistance(next.node.index, target.index);
						next.node.parent = currentNode;

						next.node.reached = next.move;

						open.add(next.node);
					} else if (currentDistance + currentNode.g < next.node.g) {
						next.node.g = currentDistance + currentNode.g;
						next.node.parent = currentNode;

						next.node.reached = next.move;

						if (open.contains(next.node))
							open.remove(next.node);

						if (closed.contains(next.node))
							closed.remove(next.node);

						open.add(next.node);
					}
				}
			}
		}

		return extractPath(target);
	}

	public synchronized int[] computePathsAStar(int s, int t, Game game) {
		return computePathsAStar(s, t, MOVE.NEUTRAL, game);
	}

	private synchronized int[] extractPath(N target) {
		ArrayList<Integer> route = new ArrayList<Integer>();
		N current = target;
		route.add(current.index);

		while (current.parent != null) {
			route.add(current.parent.index);
			current = current.parent;
		}

		Collections.reverse(route);

		int[] routeArray = new int[route.size()];

		for (int i = 0; i < routeArray.length; i++)
			routeArray[i] = route.get(i);

		return routeArray;
	}

	public void resetGraph() {
		for (N node : graph) {
			node.g = 0;
			node.h = 0;
			node.parent = null;
			node.reached = null;
		}
	}
}

class N implements Comparable<N> {
	public N parent;
	public double g, h;
	public boolean visited = false;
	public ArrayList<E> adj;
	public int index;
	public MOVE reached = null;

	public N(int index) {
		adj = new ArrayList<E>();
		this.index = index;
	}

	public N(double g, double h) {
		this.g = g;
		this.h = h;
	}

	public boolean isEqual(N another) {
		return index == another.index;
	}

	public String toString() {
		return "" + index;
	}

	public int compareTo(N another) {
		if ((g + h) < (another.g + another.h))
			return -1;
		else if ((g + h) > (another.g + another.h))
			return 1;

		return 0;
	}
}

class E {
	public N node;
	public MOVE move;
	public double cost;

	public E(N node, MOVE move, double cost) {
		this.node = node;
		this.move = move;
		this.cost = cost;
	}
}