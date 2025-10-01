#include <QApplication>                              // 1 - орёл 0 - решка
#include <ctime>
#include <random>
#include <QDebug>
#include <QVector>
#include <Qpair>
#include <QtCharts>


QPair<int, int> coinFlip100(double seed, double p){
    std::mt19937 rng(seed);
    std::bernoulli_distribution coin(p);   //шанс на орла
    QPair<int, int> headsCountANDstreak;
    headsCountANDstreak.first = 0;
    int streak = 0;
    int maxStreak = 0;
    for(int i = 0; i < 100; i++){
        int flip = coin(rng);
        if (flip == 1) {
            headsCountANDstreak.first++;
            streak++;
            if(streak > maxStreak)
                maxStreak = streak;
        }
        else {
            streak = 0;
        }
    }
    headsCountANDstreak.second = maxStreak;
    return headsCountANDstreak;
}

void insertSorted(QVector<int>& vec, int value) {
    auto it = std::lower_bound(vec.begin(), vec.end(), value);
    vec.insert(it, value);
}

int main(int argc, char *argv[])
{
    int experimentsCounts = 1000000;
    double headsAverage = 0;
    double headsAbove60 = 0;
    double streakChance = 0;
    QVector<double> intervals(10,0);
    QVector<int> Heads;
    for(int i = 0; i < experimentsCounts; i++) {
        QPair<int, int> temp = coinFlip100(i, 0.5);
        int tempHeads = temp.first;
        int tempStreaks = temp.second;
        headsAverage += tempHeads;
        insertSorted(Heads, tempHeads);
        if(tempHeads > 60) {
            headsAbove60++;                                  //[0,10) - i = 0, [10,20) - i = 1 ...
        }
        int j = tempHeads / 10;
        if(j == 10)
            intervals[9]++;
        else
            intervals[j]++;
        if(tempStreaks >= 5) {
            streakChance++;
        }
    }
    headsAverage /= experimentsCounts;
    headsAbove60 = headsAbove60 / experimentsCounts;
    streakChance = streakChance / experimentsCounts;
    for(int i = 0; i < 10; i++) {
        intervals[i] = intervals[i] / experimentsCounts;
    }
    int lowerBound = experimentsCounts * 0.025;
    int upperBound = experimentsCounts - (experimentsCounts * 0.025);


    int experimentsCountWithP = 10000;
    QVector<QVector<double>> lineData(4, QVector<double>(100));
    double headsAverageWithP = 0;
    double streakChanceWithP = 0;
    double streakAverageLengthWithP = 0;
    for(int i = 1; i <= 100; i++){
        headsAverageWithP = 0;
        streakChanceWithP = 0;
        streakAverageLengthWithP = 0;
        QVector<int> headsWithP;
        for(int j = 1; j < experimentsCountWithP; j++){
            double p = i/100.0;
            QPair<int, int> temp = coinFlip100(j, p);
            int tempHeads = temp.first;
            int tempStreaks = temp.second;
            headsAverageWithP += tempHeads;
            insertSorted(headsWithP, tempHeads);
            if(tempStreaks >= 5) {
                streakChanceWithP++;
            }
            streakAverageLengthWithP += tempStreaks;
        }
        headsAverageWithP /= experimentsCountWithP;
        lineData[0][i-1] = headsAverageWithP;
        int lowerBoundWithP = experimentsCountWithP * 0.025;
        int upperBoundWithP = experimentsCountWithP - (experimentsCountWithP * 0.025);
        lineData[1][i-1] = headsWithP[upperBoundWithP] - headsWithP[lowerBoundWithP];
        streakChanceWithP /= experimentsCountWithP;
        lineData[2][i-1] = streakChanceWithP;
        streakAverageLengthWithP /= experimentsCountWithP;
        lineData[3][i-1] = streakAverageLengthWithP;
    }


    QApplication a(argc, argv);
    QWidget window;
    QVBoxLayout *mainLayout = new QVBoxLayout(&window);

    //вывод инфы в строки
    QHBoxLayout *labelsLayout = new QHBoxLayout();
    QList<QLabel*> labels;
    for (int i = 0; i < 4; ++i) {
        QLabel *label = new QLabel();
        label->setAlignment(Qt::AlignCenter);
        label->setMaximumHeight(30);
        labels.append(label);
        labelsLayout->addWidget(label);
    }
    labels[0]->setText("1)Среднее число орлов: " + QString::number(headsAverage));
    labels[1]->setText("2)Вероятность получить число орлов больше 60: " + QString::number(headsAbove60));
    labels[2]->setText("4)Внутри интервала [" + QString::number(Heads[lowerBound]) + "," +
    QString::number(Heads[upperBound]) + "] с вероятность 0.95 стоит ожидать значение числа орлов");
    labels[3]->setText("5)Вероятность хотя бы одной серии из 5 орлов подярд: " + QString::number(streakChance));
    mainLayout->addLayout(labelsLayout);

    //диаграмма
    QBarSet *set1 = new QBarSet("");
    for (double val : intervals)
        *set1 << val;

    QBarSeries *barSeries = new QBarSeries();
    barSeries->append(set1);

    QChart *barChart = new QChart();
    barChart->addSeries(barSeries);
    barChart->setTitle("Вероятность выпадения числа орлов, принадлежащих соотвествующему интервалу");
    barChart->legend()->hide();

    QValueAxis *axisY = new QValueAxis();
    axisY->setRange(0, 0.6);
    barChart->addAxis(axisY, Qt::AlignLeft);
    barSeries->attachAxis(axisY);

    QStringList categories;
    for (int i = 0; i < 100; i += 10) {
        if (i < 90)
            categories << QString("[%1,%2)").arg(i).arg(i+10);
        else
            categories << QString("[%1,%2]").arg(i).arg(i+10);
    }

    QBarCategoryAxis *axisX = new QBarCategoryAxis();
    axisX->append(categories);
    barChart->addAxis(axisX, Qt::AlignBottom);
    barSeries->attachAxis(axisX);

    QChartView *barView = new QChartView(barChart);
    barView->setRenderHint(QPainter::Antialiasing);

    QGridLayout *chartsLayout = new QGridLayout();
    chartsLayout->addWidget(barView, 0, 0, 1, 2);

    //графики
    QVector<QString> names = {"Среденее число орлов", "Интервал внутри которого с вероятность 0.95 стоит ожидать значение числа орлов",
                              "Вероятность наличия серии из 5 орлов", "Длинна максимальной серии"};
    for (int i = 0; i < lineData.size(); ++i) {
        QLineSeries *line = new QLineSeries();
        for (int j = 0; j < lineData[i].size(); ++j)
            line->append((j+1)/100.0 , lineData[i][j]);

        QChart *lineChart = new QChart();
        lineChart->addSeries(line);
        lineChart->setTitle(names[i]);
        lineChart->legend()->hide();

        QValueAxis *axisX = new QValueAxis();
        axisX->setRange(0.0, 1.0);
        axisX->setTickCount(11);
        axisX->setLabelFormat("%.1f");
        lineChart->addAxis(axisX, Qt::AlignBottom);
        line->attachAxis(axisX);

         QValueAxis *axisY = new QValueAxis();
        if (i == 1) {
            axisY->setRange(0, 25);
            axisY->setTickCount(6);
            axisY->setLabelFormat("%d");
        }
        if (i == 2) {
            axisY->setRange(0, 1);
            axisY->setTickCount(6);
            axisY->setLabelFormat("%.1f");
        }
        if (i == 0 || i == 3) {
            axisY->setRange(0, 100);
            axisY->setTickCount(6);
            axisY->setLabelFormat("%d");
        }
        lineChart->addAxis(axisY, Qt::AlignLeft);
        axisY->setVisible(true);
        line->attachAxis(axisY);
        QChartView *lineView = new QChartView(lineChart);
        lineView->setRenderHint(QPainter::Antialiasing);

        chartsLayout->addWidget(lineView, 1 + i/2, i%2);
    }

    mainLayout->addLayout(chartsLayout);

    window.resize(1200, 900);
    window.show();
    return a.exec();
    }


