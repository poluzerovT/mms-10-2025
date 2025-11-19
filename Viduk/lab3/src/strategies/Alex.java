package strategies;

public class Alex extends Strategies {

	public Alex() {
		super("Alex");
	}

	public void current_move(Strategies other, int turn) {

		if (this.moves.size() > 100)
			return;
		for (int i = 0; i < 200; i++) {
			this.moves.add(1);
		}
	}
}