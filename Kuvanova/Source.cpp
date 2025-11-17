#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <random>
#include <numeric>
#include <iomanip>
#include <cmath>
#include <map>

const int PAYOFF[2][2] = { {3, 0}, {5, 1} };
const int ROUNDS = 200;
const int SIMULATIONS = 1000;

std::random_device rd;
std::mt19937 gen(rd());

class Strategy {
public:
    virtual ~Strategy() = default;
    virtual int play(const std::vector<int>& my_history, const std::vector<int>& opp_history) = 0;
    virtual std::string getName() const = 0;
    virtual void reset() {}
};

// Детерминированные стратегии
class Alex : public Strategy {
public:
    int play(const std::vector<int>&, const std::vector<int>&) override { return 1; }
    std::string getName() const override { return "Alex"; }
};

class Bob : public Strategy {
public:
    int play(const std::vector<int>&, const std::vector<int>&) override { return 0; }
    std::string getName() const override { return "Bob"; }
};

class Clara : public Strategy {
public:
    int play(const std::vector<int>&, const std::vector<int>& opp_history) override {
        return opp_history.empty() ? 0 : opp_history.back();
    }
    std::string getName() const override { return "Clara"; }
};

class Denis : public Strategy {
public:
    int play(const std::vector<int>&, const std::vector<int>& opp_history) override {
        return opp_history.empty() ? 0 : 1 - opp_history.back();
    }
    std::string getName() const override { return "Denis"; }
};

class Emma : public Strategy {
public:
    int play(const std::vector<int>& my_history, const std::vector<int>&) override {
        return (my_history.size() + 1) % 20 == 0 ? 1 : 0;
    }
    std::string getName() const override { return "Emma"; }
};

class Frida : public Strategy {
    bool betrayed = false;
public:
    int play(const std::vector<int>&, const std::vector<int>& opp_history) override {
        if (!opp_history.empty() && opp_history.back() == 1) betrayed = true;
        return betrayed ? 1 : 0;
    }
    std::string getName() const override { return "Frida"; }
    void reset() override { betrayed = false; }
};

class George : public Strategy {
    int counter = 0;
public:
    int play(const std::vector<int>& my_history, const std::vector<int>& opp_history) override {
        counter++;
        if (counter <= 2) return 0;
        return opp_history.empty() ? 0 : 1 - opp_history.back();
    }
    std::string getName() const override { return "George"; }
    void reset() override { counter = 0; }
};

// Стохастические стратегии
class Hank : public Strategy {
    std::uniform_real_distribution<double> dist{ 0.0, 1.0 };
public:
    int play(const std::vector<int>&, const std::vector<int>&) override {
        return dist(gen) < 0.5 ? 0 : 1;
    }
    std::string getName() const override { return "Hank"; }
};

class Ivan : public Strategy {
    std::uniform_real_distribution<double> dist{ 0.0, 1.0 };
public:
    int play(const std::vector<int>&, const std::vector<int>&) override {
        return dist(gen) < 0.9 ? 0 : 1;
    }
    std::string getName() const override { return "Ivan"; }
};

class Jack : public Strategy {
    std::uniform_real_distribution<double> dist{ 0.0, 1.0 };
public:
    int play(const std::vector<int>&, const std::vector<int>& opp_history) override {
        if (opp_history.empty()) return 0;
        if (opp_history.back() == 0) return 1;
        return dist(gen) < 0.25 ? 0 : 1;
    }
    std::string getName() const override { return "Jack"; }
};

class Kevin : public Strategy {
    std::uniform_real_distribution<double> dist{ 0.0, 1.0 };
public:
    int play(const std::vector<int>&, const std::vector<int>& opp_history) override {
        if (opp_history.empty()) return 0;
        int last = opp_history.back();
        return dist(gen) < 0.25 ? 1 - last : last;
    }
    std::string getName() const override { return "Kevin"; }
};

class Lucas : public Strategy {
    int period, counter = 0;
    std::uniform_int_distribution<int> dist{ 1, 50 };
public:
    Lucas() : period(dist(gen)) {}
    int play(const std::vector<int>&, const std::vector<int>&) override {
        counter++;
        return counter % period == 0 ? 1 : 0;
    }
    std::string getName() const override { return "Lucas"; }
    void reset() override { period = dist(gen); counter = 0; }
};

class Max : public Strategy {
    int length, move = 0, count = 0;
    std::uniform_int_distribution<int> dist{ 0, 20 };
public:
    Max() : length(dist(gen)) {}
    int play(const std::vector<int>&, const std::vector<int>&) override {
        if (count >= length) {
            move = 1 - move;
            length = dist(gen);
            count = 0;
        }
        count++;
        return move;
    }
    std::string getName() const override { return "Max"; }
    void reset() override { length = dist(gen); move = count = 0; }
};

class Natan : public Strategy {
    std::uniform_real_distribution<double> dist{ 0.0, 1.0 };
public:
    int play(const std::vector<int>&, const std::vector<int>& opp_history) override {
        if (opp_history.empty()) return 0;//начинаем с 0
        double base_prob = 0.5;
        if (opp_history.back() == 0) {// если оппонент кооперировал
            base_prob = 0.6; 
        }
        else {
            base_prob = 0.4; 
        }

        return dist(gen) < base_prob ? 0 : 1;
    }
    
    std::string getName() const override { return "Natan"; }
};

struct GameResult {
    int scoreA, scoreB;
};

GameResult playGame(Strategy* a, Strategy* b) {
    std::vector<int> histA, histB;
    GameResult res = { 0, 0 };

    for (int i = 0; i < ROUNDS; i++) {
        int moveA = a->play(histA, histB);
        int moveB = b->play(histB, histA);

        histA.push_back(moveA);
        histB.push_back(moveB);

        res.scoreA += PAYOFF[moveA][moveB];
        res.scoreB += PAYOFF[moveB][moveA];
    }
    return res;
}

struct Statistics {
    double mean;
    double median;
    double mode;
    double variance;
};

Statistics calculateStats(const std::vector<int>& data) {
    Statistics stats = { 0, 0, 0, 0 };
    if (data.empty()) return stats;

    // Среднее значение
    stats.mean = std::accumulate(data.begin(), data.end(), 0.0) / data.size();

    // Медиана
    std::vector<int> sorted = data;
    std::sort(sorted.begin(), sorted.end());
    if (sorted.size() % 2 == 0) {
        stats.median = (sorted[sorted.size() / 2 - 1] + sorted[sorted.size() / 2]) / 2.0;
    }
    else {
        stats.median = sorted[sorted.size() / 2];
    }

    // Мода 
    int k = std::log2(1 + data.size()); // число интервалов
    if (k < 1) k = 1;

    double min_val = *std::min_element(data.begin(), data.end());
    double max_val = *std::max_element(data.begin(), data.end());
    double bin_width = (max_val - min_val) / k;

    if (bin_width > 0) {
        std::vector<int> histogram(k, 0);
        for (int x : data) {
            int bin_index = (x - min_val) / bin_width;
            if (bin_index >= k) bin_index = k - 1;
            if (bin_index < 0) bin_index = 0;
            histogram[bin_index]++;
        }

        int max_bin_index = std::distance(histogram.begin(),
            std::max_element(histogram.begin(), histogram.end()));
        stats.mode = min_val + (max_bin_index + 0.5) * bin_width;
    }
    else {
        stats.mode = stats.mean;
    }

    // Дисперсия
    double sum_sq = 0.0;
    for (int x : data) {
        sum_sq += (x - stats.mean) * (x - stats.mean);
    }
    stats.variance = data.size() > 1 ? sum_sq / (data.size() - 1) : 0;

    return stats;
}

void printStatisticsTable(const std::vector<Strategy*>& strategies) {
    std::cout << "ТАБЛИЦА СТАТИСТИКИ ДЛЯ СТОХАСТИЧЕСКИХ СТРАТЕГИЙ\n";
    std::cout << "==================================================\n\n";

    std::vector<Strategy*> stochastic_strategies;
    for (auto* s : strategies) {
        std::string name = s->getName();
        if (name == "Hank" || name == "Ivan" || name == "Jack" || name == "Kevin" ||
            name == "Lucas" || name == "Max" || name == "Natan") {
            stochastic_strategies.push_back(s);
        }
    }

    // Для каждой стохастической стратегии против всех остальных
    for (auto* strat : stochastic_strategies) {
        std::cout << "СТРАТЕГИЯ: " << strat->getName() << "\n";
        std::cout << std::string(60, '-') << "\n";
        std::cout << std::left << std::setw(10) << "Оппонент"
            << std::setw(10) << "Среднее"
            << std::setw(10) << "Медиана"
            << std::setw(10) << "Мода"
            << std::setw(10) << "Дисперсия" << "\n";
        std::cout << std::string(60, '-') << "\n";

        for (auto* opponent : strategies) {
            if (strat == opponent) continue;

            std::vector<int> scores;
            for (int sim = 0; sim < SIMULATIONS; sim++) {
                strat->reset();
                opponent->reset();
                GameResult res = playGame(strat, opponent);
                scores.push_back(res.scoreA);
            }

            Statistics stats = calculateStats(scores);

            std::cout << std::left << std::setw(10) << opponent->getName()
                << std::fixed << std::setprecision(1)
                << std::setw(10) << stats.mean
                << std::setw(10) << stats.median
                << std::setw(10) << stats.mode
                << std::setw(10) << stats.variance << "\n";
        }
        std::cout << "\n";
    }
}

void printComparisonTable(const std::vector<Strategy*>& strategies) {
    std::cout << "ТАБЛИЦА СРАВНЕНИЯ ВСЕХ СТРАТЕГИЙ (СРЕДНИЕ ЗНАЧЕНИЯ)\n";
    std::cout << "===================================================\n\n";

    
    std::cout << std::left << std::setw(8) << "";
    for (auto* s : strategies) {
        std::cout << std::setw(8) << s->getName();
    }
    std::cout << "\n" << std::string(8 * (strategies.size() + 1), '-') << "\n";


    for (auto* row_strat : strategies) {
        std::cout << std::left << std::setw(8) << row_strat->getName();

        for (auto* col_strat : strategies) {
            if (row_strat == col_strat) {
                std::cout << std::setw(8) << "X";
            }
            else {
                std::vector<int> scores;
                int simulations = 1;

                
                std::string row_name = row_strat->getName();
                std::string col_name = col_strat->getName();
                if (row_name == "Hank" || row_name == "Ivan" || row_name == "Jack" ||
                    row_name == "Kevin" || row_name == "Lucas" || row_name == "Max" || row_name == "Natan" ||
                    col_name == "Hank" || col_name == "Ivan" || col_name == "Jack" ||
                    col_name == "Kevin" || col_name == "Lucas" || col_name == "Max" || col_name == "Natan") {
                    simulations = SIMULATIONS;
                }

                for (int sim = 0; sim < simulations; sim++) {
                    row_strat->reset();
                    col_strat->reset();
                    GameResult res = playGame(row_strat, col_strat);
                    scores.push_back(res.scoreA);
                }

                double mean = std::accumulate(scores.begin(), scores.end(), 0.0) / scores.size();
                std::cout << std::fixed << std::setprecision(0) << std::setw(8) << mean;
            }
        }
        std::cout << "\n";
    }
}

int main() {
    setlocale(LC_ALL, "RU");

    std::vector<Strategy*> strategies = {
        new Alex(), new Bob(), new Clara(), new Denis(), new Emma(), new Frida(), new George(),
        new Hank(), new Ivan(), new Jack(), new Kevin(), new Lucas(), new Max(), new Natan()
    };

    std::cout << "ЛАБОРАТОРНАЯ РАБОТА №3 \n";
    std::cout << "==================================================\n\n";

    printComparisonTable(strategies);
    std::cout << "\n\n";
    printStatisticsTable(strategies);

   
    for (auto s : strategies) delete s;
    return 0;
}