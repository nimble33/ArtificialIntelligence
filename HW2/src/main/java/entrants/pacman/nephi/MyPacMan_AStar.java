package entrants.pacman.nephi;
import pacman.controllers.PacmanController;
import pacman.game.Game;
import pacman.game.Constants.MOVE;

import java.util.ArrayList;
import java.util.Random;

import static pacman.game.Constants.*;


// Code taken from Examples - POPacMan.java
// Astar - Applicable only to PacMan

public class MyPacMan_AStar extends PacmanController {
    private static final int MIN_DISTANCE = 20;
    private Random random = new Random();
    private MOVE myMove;
    @Override
    public MOVE getMove(Game game, long timeDue) {

        // Should always be possible as we are PacMan
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
       // System.out.println(targets.get(10));
        //Choose an Index for destination
        int closestIndex = game.getClosestNodeIndexFromNodeIndex(current,targetsArray, DM.PATH);
        
        //Compute the best path using A* Algorithm src=current, dst=closestIndex,game
        
        int[] path=computeAStarPath(current,closestIndex,game);
        
      
		return myMove;


        
    }
	private int[] computeAStarPath(int current, int closestIndex, Game game) {
		// TODO Auto-generated method stub
		return null;
	}
}
