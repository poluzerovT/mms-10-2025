package Orel_i_reshka;

import java.util.Locale;
import java.util.Random;
import java.util.Scanner;
import java.io.PrintWriter;
import java.util.Arrays;
import java.io.IOException;

public class Orel_i_reshka {

	static int[][] experimenti = new int[1000000][100];
	static int itogi[] = new int[1000000];

	public static int orel_or_reshka(double probability) {
		Random rand = new Random();
		if (rand.nextDouble() <= probability)
			return 1;
		else
			return 0;
	}

	public static void experiment(double probability) {
		for (int i = 0; i < 1000000; i++) {
			for (int j = 0; j < 100; j++) {
				experimenti[i][j] = orel_or_reshka(probability);
			}
		}
	}

	public static double srednee(int f) {
		double a = 0, b = 0;
		for (int i = 0; i < 1000000; i++) {
			for (int j = 0; j < 100; j++) {
				if (experimenti[i][j] == 1) {
					a++;
					b++;
				}
			}
			itogi[i] += b;
			b = 0;
		}
		Arrays.sort(itogi);
		if (f == 1)
			System.out.println("from " + itogi[24999] + " to " + itogi[975000]);
		return (double) a / 1000000;
	}

	public static void intervali() {
		int[] a = new int[10];
		int kol = 0;
		for (int i = 0; i < 1000000; i++) {
			for (int j = 0; j < 100; j++) {
				if (experimenti[i][j] == 1)
					kol++;
				;
			}
			for (int j = 0; j < 10; j++) {
				if (kol > j * 10 && kol < j * 10 + 10)
					a[j]++;
			}
			kol = 0;
		}
		for (int i = 0; i < 10; i++) {
			System.out.println((double) a[i] / 10000);
		}
	}

	public static void podrad() {
		int a = 0;
		int b;
		for (int i = 0; i < 1000000; i++) {
			b = 0;
			for (int j = 0; j < 100; j++) {
				if (experimenti[i][j] == 1)
					b++;
				else
					b = 0;
				if (b == 5) {
					a++;
					j = 100;
				}
			}
		}
		System.out.println((double) a / 10000);
	}

	public static void main(String[] args) {
		Scanner input = new Scanner(System.in).useLocale(Locale.US);
		try (PrintWriter writer = new PrintWriter("file.txt")) {

			experiment(0.5);
			double a = srednee(1);
			System.out.println(a);
			intervali();
			podrad();
			for (int i = 0; i < 1000; i++) {
				experiment((double) i / 1000);
				writer.println((int)srednee(0));
			}
			input.close();
			writer.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
