//import examples.poPacMan.POPacMan;
import entrants.pacman.username.MyPacMan;
import examples.commGhosts.POCommGhosts;
import pacman.Executor;


/**
 * Created by pwillic on 06/05/2016.
 */
public class Main {

    public static void main(String[] args) {

        Executor executor = new Executor(true, true);

        executor.runGameTimed(new MyPacMan(), new POCommGhosts(50), true);
    }
}
