package strategies;

import java.util.Random;

public class Natan extends Strategies {

	public Natan() {
		super("Natan");
	}

	public void current_move(Strategies other, int turn) {

		Random rand = new Random();
		if (rand.nextInt(100) % 7 > 2)
			this.moves.add(0);
		else
			this.moves.add(1);
	}

}
