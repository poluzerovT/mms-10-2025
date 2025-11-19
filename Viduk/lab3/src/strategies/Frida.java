package strategies;

public class Frida extends Strategies {

	public Frida() {
		super("Frida");
	}

	public void current_move(Strategies other, int turn) {

		if (this.moves.size() == 200)
			return;
		if (this.moves.size() == 0) {
			this.moves.add(0);
			return;
		}
		if (other.moves.get(other.moves.size() - 1 - turn) == 0) {
			this.moves.add(0);
			return;
		}
		for (int i = this.moves.size(); i < 200; i++) {
			this.moves.add(1);
		}
	}
}