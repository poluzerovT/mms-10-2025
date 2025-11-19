package strategies;

public class Bob extends Strategies {

	public Bob() {
		super("Bob");
	}

	public void current_move(Strategies other, int turn) {

		if (this.moves.size() > 100)
			return;
		for (int i = 0; i < 200; i++) {
			this.moves.add(0);
		}
	}
}