package strategies;

import java.util.Random;

public class Kevin extends Strategies {

	public Kevin() {
		super("Kevin");
	}

	public void current_move(Strategies other, int turn) {

		if (this.moves.size() == 0) {
			this.moves.add(0);
			return;
		}
		Random rand = new Random();
		if (rand.nextDouble() <= 0.25)
			this.moves.add(other.moves.get(other.moves.size() - turn - 1) == 0 ? 1 : 0);
		else
			this.moves.add(other.moves.get(other.moves.size() - turn - 1));
	}
}