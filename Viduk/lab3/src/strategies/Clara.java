package strategies;

public class Clara extends Strategies {

	public Clara() {
		super("Clara");
	}

	public void current_move(Strategies other, int turn) {

		if (this.moves.size() == 0) {
			this.moves.add(0);
			return;
		}
		this.moves.add(other.moves.get(other.moves.size() - 1 - turn));
	}

}