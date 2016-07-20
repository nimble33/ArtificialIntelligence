import pacman.Executor;
import entrants.pacman.nephi.MyPacMan_BFS;
//import entrants.pacman.nephi.MyPacMan_GBFS;
import entrants.pacman.nephi.MyPacMan;
import entrants.pacman.nephi.MyPacMan_AStar;
import entrants.pacman.nephi.MyPacMan_DFS;
import entrants.pacman.nephi.MyPacMan_GBFS;
import examples.commGhosts.POCommGhosts;
import pacman.controllers.examples.RandomGhosts;
/**
 * Created by pwillic on 06/05/2016.
 */
public class Main {

	public static void main(String[] args) {



		//Default
		//Partially Observable
		//Executor executor = new Executor(true, true);
		//executor.runGameTimed(new MyPacMan(), new POCommGhosts(50), true);

		//1.DFS Implementation - Uninformed Search
		//Partially Observable
		//Executor executor = new Executor(true, true);
		//executor.runGameTimed(new MyPacMan_DFS(), new RandomGhosts(), true);

		//4.Greedy BFS - Informed Search
		//Fully Observable
		Executor executor = new Executor(false, true);
		executor.runGameTimed(new MyPacMan_GBFS(), new POCommGhosts(50), true);


	}
}
