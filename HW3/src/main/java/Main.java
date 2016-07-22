import pacman.Executor;
import entrants.pacman.nephi.MyPacMan_Adversarial;
import examples.commGhosts.POCommGhosts;

/**
 * Created by pwillic on 06/05/2016.
 */
public class Main {

	public static void main(String[] args) {



		//Default
		//Partially Observable
		//Executor executor = new Executor(true, true);
		//executor.runGameTimed(new MyPacMan(), new POCommGhosts(50), true);

		//Fully Observable
		Executor executor = new Executor(false, true);
		executor.runGameTimed(new MyPacMan_Adversarial(), new POCommGhosts(50), true);



	}
}
