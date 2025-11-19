package strategies;

import java.util.Random;

public class Max extends Strategies {

	public Max() {
		super("Max");
	}

	public void current_move(Strategies other, int turn) {

		if (this.moves.size() > 100)
			return;
		Random rand = new Random();
		for (int sum = 0; sum < 200;) {
			int n = rand.nextInt(21);
			sum += n;
			for (int i = 0; i < n; i++)
				this.moves.add(0);
			n = rand.nextInt(21);
			sum += n;
			for (int i = 0; i < n; i++)
				this.moves.add(1);
		}
	}
}