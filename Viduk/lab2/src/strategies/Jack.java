package strategies;

import java.util.Random;

public class Jack extends Strategies {

	public Jack() {
		super("Jack");
	}

	public void current_move(Strategies other, int turn) {

		if (this.moves.size() == 0) {
			this.moves.add(0);
			return;
		}
		if (other.moves.get(other.moves.size() - 1 - turn) == 0) {
			this.moves.add(0);
		} else {
			Random rand = new Random();
			if (rand.nextDouble() <= 0.25)
				this.moves.add(0);
			else
				this.moves.add(1);
		}
	}

}
