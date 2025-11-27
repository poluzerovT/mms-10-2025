package strategies;

public class Emma extends Strategies {

	public Emma() {
		super("Emma");
	}

	public void current_move(Strategies other, int turn) {

		if ((this.moves.size() + 1) % 20 == 0)
			this.moves.add(1);
		this.moves.add(0);
	}

}