package main;

import strategies.*;
import java.util.ArrayList;

public class Main {

	public static void main(String args[]) {

		ArrayList<Strategies> tornament = new ArrayList<>();

		tornament.add(new Hank());
		tornament.add(new Ivan());
		tornament.add(new Jack());
		tornament.add(new Kevin());
		tornament.add(new Lucas());
		tornament.add(new Max());
		tornament.add(new Natan());
		tornament.add(new Alex());
		tornament.add(new Bob());
		tornament.add(new Clara());
		tornament.add(new Denis());
		tornament.add(new Emma());
		tornament.add(new Frida());

		for (int i = 0; i < tornament.size() - 1; i++)
			for (int j = i + 1; j < tornament.size(); j++) {
				tornament.get(i).judje(tornament.get(j), 100000);
				System.out.println();
			}
		for (int i = 0; i < tornament.size() - 1; i++)
			System.out.printf("%s, количество побед = %d\n", tornament.get(i).name, tornament.get(i).victories);
	}

}
