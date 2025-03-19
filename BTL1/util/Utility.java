
public class Utility {

	/**
	 * Test whether a specific number is a prime number.
	 * 
	 * @param num
	 *            the number
	 * @return <code>true</code> if <code>num</code> is a prime number.
	 */
	public static boolean isPrime(int num) {
		if (num < 2) {
			return false;
		}
		for (int i = 2; i < num / 2; i++) {
			if (num % i == 0) {
				return false;
			}
		}
		return true;
	}

	/**
	 * Test whether a specific number is a square number.
	 * 
	 * @param num
	 *            the number
	 * @return <code>true</code> if <code>num</code> is a square number.
	 */
	public static boolean isSquare(int num) {
		int x = (int) Math.sqrt(num);
		return x * x == num;
	}

	/**
	 * Test whether a specific number is a fibonacci number.
	 * 
	 * @param num
	 *            the number
	 * @return <code>true</code> if <code>num</code> is a cube number.
	 */
	public static int isFibonacci(int num) {
		if (num <= 2)
			return -1;
		int a = 0, b = 1, i = 1;
		while (b < num) {
			int c = a + b;
			a = b;
			b = c;
			i++;
		}
		return b == num ? i : -1;
	}
}
