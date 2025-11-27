package strategies;

import java.util.ArrayList;
import java.util.Collections;

public abstract class Strategies {

	public String name;
	int count;
	public int victories;
	ArrayList<Integer> moves;
	ArrayList<ArrayList<Integer>> wins;

	private static int results[][] = { { 0, 0, 1 }, { 0, 3, 5 }, { 1, 0, 1 } };

	Strategies(String n) {
		this.name = n;
		this.count = 0;
		this.victories = 0;
		this.wins = new ArrayList<>();
	}

	public abstract void current_move(Strategies other, int turn);

	public void judje(Strategies other, int n) {
		
		ArrayList<Integer> player1 = new ArrayList<>();
		ArrayList<Integer> player2 = new ArrayList<>();

		for (int l = 0; l < n; l++) {
			
			this.moves = new ArrayList<>();
			other.moves = new ArrayList<>();
			
			for(int j = 0; j < 200; j++) {
				this.current_move(other, 0);
				other.current_move(this, 1);
			}
			
			int a, b;
			player1.add(0);
			player2.add(0);
			for (int i = 0; i < 200; i++) {
				a = this.moves.get(i) == 1 ? 1 : 2;
				b = other.moves.get(i) == 1 ? 1 : 2;
				player1.set(l, player1.get(0) + results[a][b]);
				player2.set(l, player2.get(0) + results[b][a]);
			}
			
		}
		int sum1 = 0, sum2 = 0, deviation1 = 0, deviation2 = 0;
		for (int num : player1) {
		    sum1 += num;
		}
		for (int num : player2) {
		    sum2 += num;
		}
		sum1 /= n;
		sum2 /= n;
		for (int num : player1) {
		    deviation1 += Math.pow(sum1 - num, 2);
		}
		for (int num : player2) {
			deviation2 += Math.pow(sum2 - num, 2);
		}
		deviation1 /= n;
		deviation2 /= n;
		
		Collections.sort(player1);
		Collections.sort(player2);
		
		int k1 = (int) Math.round(Math.log(1 + player1.size()) / Math.log(2));
		int k2 = (int) Math.round(Math.log(1 + player2.size()) / Math.log(2));

		int max1 = player1.get(player1.size() - 1);
		int min1 = player1.get(0);
		int min2 = player2.get(0);
		int max2 = player2.get(player2.size() - 1);

		double intervalWidth1 = (double)(max1 - min1) / k1;
		double intervalWidth2 = (double)(max2 - min2) / k2;

		int[] freq1 = new int[k1];
		int[] freq2 = new int[k2];

		for (int num : player1) {
		    int index = Math.min((int)((num - min1) / intervalWidth1), k1 - 1);
		    freq1[index]++;
		}

		for (int num : player2) {
		    int index = Math.min((int)((num - min2) / intervalWidth2), k2 - 1);
		    freq2[index]++;
		}

		int maxFreqIndex1 = 0, maxFreqIndex2 = 0;
		for (int i = 1; i < k1; i++) {
		    if (freq1[i] > freq1[maxFreqIndex1]) maxFreqIndex1 = i;
		}
		for (int i = 1; i < k2; i++) {
		    if (freq2[i] > freq2[maxFreqIndex2]) maxFreqIndex2 = i;
		}

		double modalStart1 = min1 + maxFreqIndex1 * intervalWidth1;
		double modalEnd1 = modalStart1 + intervalWidth1;
		double modalStart2 = min2 + maxFreqIndex2 * intervalWidth2;
		double modalEnd2 = modalStart2 + intervalWidth2;

		double sumModal1 = 0, sumModal2 = 0;
		int countModal1 = 0, countModal2 = 0;

		for (int num : player1) {
		    if (num >= modalStart1 && num < modalEnd1) {
		        sumModal1 += num;
		        countModal1++;
		    }
		}

		for (int num : player2) {
		    if (num >= modalStart2 && num < modalEnd2) {
		        sumModal2 += num;
		        countModal2++;
		    }
		}

		double mode1 = sumModal1 / countModal1;
		double mode2 = sumModal2 / countModal2;
		if(sum1 > sum2) this.victories++;
		else other.victories++;
		System.out.printf("%s VS %s\n", this.name, other.name);
		System.out.printf("Среднее значение: %d   %d\n", sum1, sum2);
		System.out.printf("Дисперсия: %d   %d\n", deviation1, deviation2);
		System.out.printf("Медиана: %d   %d\n", player1.get(n / 2), player2.get(n / 2));
		System.out.printf("Мода: %f   %f\n", mode1, mode2);
		
	}
}