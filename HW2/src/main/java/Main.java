import pacman.Executor;
import entrants.pacman.nephi.MyPacMan_BFS;
import entrants.pacman.nephi.MyPacMan_AStar;
import entrants.pacman.nephi.MyPacMan_DFS;
import examples.commGhosts.POCommGhosts;
import pacman.controllers.examples.RandomGhosts;
/**
 * Created by pwillic on 06/05/2016.
 */
public class Main {

	public static void main(String[] args) {

		Executor executor = new Executor(true, true);
		//Default
		//executor.runGameTimed(new POPacMan(), new POCommGhosts(50), true);
		
		//1.DFS Implementation - Uninformed Search
		executor.runGameTimed(new MyPacMan_DFS(), new RandomGhosts(), true);

		//2.BFS Implementation - Uninformed Search
		// executor.runGameTimed(new MyPacMan_BFS(), new POCommGhosts(50), true);
		
		//3.AStar Implementation - Informed Search
		//executor.runGameTimed(new MyPacMan_AStar(), new StarterGhosts(), true);
		
	}
}
