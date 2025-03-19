public class Paladin extends Knight {

	public Paladin(int baseHp, int wp) {
		super(baseHp, wp);
	}

	@Override
	public double getCombatScore() {
		int n = Utility.isFibonacci(getBaseHp());
		return n != -1 ? 1000 + n : getBaseHp() * 3;
	}
}
