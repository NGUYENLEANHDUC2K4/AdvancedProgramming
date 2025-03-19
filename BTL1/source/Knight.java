public class Knight extends Fighter {

    public Knight(int baseHp, int wp) {
        super(baseHp, wp);
    }

    @Override
    public double getCombatScore() {
        double combatScore = Utility.isSquare(Battle.GROUND) ? getBaseHp() * 2
                : ((getWp() == 1) ? getBaseHp() : getBaseHp() / 10);
        return combatScore > 999 ? 999 : combatScore;
    }
}
