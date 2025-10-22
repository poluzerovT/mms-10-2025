#include <iostream>
#include <vector>
#include <iomanip>

using namespace std;

const int rounds = 200;

vector<vector<int>> W = { { 3 , 0 },
                          { 5 , 1 } 
};

struct GameResult{
    string name;
    int points = 0;
    int maxSeries = 0;
};

enum StrategyType {
    Alex,
    Bob,
    Clara,
    Denis,
    Emma,
    Frida,
    George
};

string StrategyTypeToString(StrategyType a) {
    switch (a) {
    case Alex: return "Alex";
    case Bob: return "Bob";
    case Clara: return "Clara";
    case Denis: return "Denis";
    case Emma: return "Emma";
    case Frida: return "Frida";
    case George: return "George";
    }
}

int alex(const vector<int>& opp, int round) {
    return 1;
}

int bob(const vector<int>& opp, int round) {
    return 0;
}

int clara(const vector<int>& opp, int round) {
    return (round == 1 ? 0 : opp.back());
}

int denis(const vector<int>& opp, int round) {
    return (round == 1 ? 0 : 1 - opp.back());
}

int emma(const vector<int>& opp, int round) {
    return (round % 20 == 0 ? 1 : 0);
}

int frida(const vector<int>& opp, int round) {
    if(round == 1)
        return 0;
    for (int x : opp)
        if (x == 1)
            return 1;
    return 0;
}

int george(const vector<int>& opp, int round) {
    if (round < 4)
        return 0; 
    if (opp[round - 2] + opp[round - 3] + opp[round-4] == 3)
        return 1;
    else
        return 0;
}

int move(StrategyType a, const vector<int>& opp, int round) {     
    switch (a) {
    case Alex: return alex(opp, round);
    case Bob: return bob(opp, round);
    case Clara: return clara(opp, round);
    case Denis: return denis(opp, round);
    case Emma: return emma(opp, round);
    case Frida: return frida(opp, round);
    case George: return george(opp, round);
    }
}

GameResult play(StrategyType a, StrategyType b) {         
    GameResult res;
    res.name = StrategyTypeToString(a);
    vector<int> moves;
    vector<int> movesP2;
    int domSer = 0;
    for (int i = 1; i <= rounds; i++) {
        int x = move(a, movesP2, i);
        int y = move(b, moves, i);

        moves.push_back(x);
        movesP2.push_back(y);

        int score = W[x][y];
        int scoreP2 = W[y][x];
        res.points += score;

        if (score == 5 && scoreP2 == 0)
            domSer++;
        else
            domSer = 0;
        res.maxSeries = max(res.maxSeries, domSer);
    }
    return res;
}
                                  
int main()
{
    vector<StrategyType> players{ Alex, Bob, Clara, Denis, Emma, Frida, George };
    vector<vector<GameResult>> results(players.size(), vector<GameResult>(players.size()));
    int totalPoints;
    for (int i = 0; i < players.size(); i++) {
        for (int j = 0; j < players.size(); j++) {
            results[i][j] = play(players[i], players[j]);
        }
    }
    size_t maxLen = 0;
    for (auto p : players)
        maxLen = max(maxLen, StrategyTypeToString(p).size());

    int nameColWidth = max(maxLen + 4, size_t(10)); 
    int cellWidth = 8;                             

    cout << left << setw(nameColWidth) << "Player"; 
    for (auto p : players)
        cout << right << setw(cellWidth) << StrategyTypeToString(p);
    cout << right << setw(cellWidth + 7) << "Total points";
    cout << endl;

    cout << string(nameColWidth + cellWidth * players.size() + 15, '-') << endl;

    for (int i = 0; i < players.size(); i++) {
        cout << left << setw(nameColWidth) << StrategyTypeToString(players[i]);
        totalPoints = 0;
        for (int j = 0; j < players.size(); j++) {
            cout << right << setw(cellWidth) << results[i][j].points;
            if(i != j)
            totalPoints += results[i][j].points;
        }
        cout << right << setw(cellWidth+3) << totalPoints << endl;
    }

    cout << string(nameColWidth + cellWidth * players.size() + 15, '-') << endl << endl;

    cout << left << setw(nameColWidth) << "Player";
    for (auto p : players)
        cout << right << setw(cellWidth) << StrategyTypeToString(p);
    cout << endl;

    cout << string(nameColWidth + cellWidth * players.size(), '-') << endl;

    for (int i = 0; i < players.size(); i++) {
        cout << left << setw(nameColWidth) << StrategyTypeToString(players[i]);
        for (int j = 0; j < players.size(); j++) {
            cout << right << setw(cellWidth) << results[i][j].maxSeries;
        }
        cout << endl;
    }
    return 0;
}


