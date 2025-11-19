package strategies;

import java.util.Random;

public class Ivan extends Strategies {

	public Ivan() {
		super("Ivan");
	}
	
	public void current_move(Strategies other, int turn) {
		
		Random rand = new Random();
		if(rand.nextDouble() <= 0.9)
			this.moves.add(0);
		else
			this.moves.add(1);
	}
	
}
