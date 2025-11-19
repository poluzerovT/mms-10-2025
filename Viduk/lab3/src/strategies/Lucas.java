package strategies;

import java.util.Random;

public class Lucas extends Strategies {

	public Lucas() {
		super("Lucas");
	}

	public void current_move(Strategies other, int turn) {

		if (this.moves.size() < 10) {
			Random rand = new Random();
			int n = rand.nextInt(51);
			for (int i = 0; i < n; i++)
				this.moves.add(1);
			for (int i = n; i < 200; i++)
				this.moves.add(0);
		} else
			return;
	}
}