package strategies;

import java.util.Random;

public class Hank extends Strategies {

	public Hank() {
		super("Hank");
	}
	
	public void current_move(Strategies other, int turn) {
		
		Random rand = new Random();
		if(rand.nextDouble() <= 0.5)
			this.moves.add(1);
		else
			this.moves.add(0);
	}
	
}
