from matplotlib import pyplot as plt
from matplotlib import ticker, cm

## 日本語表示用にフォント設定
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Meiryo"]

## 消費ライフボーナスリスト、ライブ報酬リスト、イベント報酬リストの作成
lb_list = [i for i in range(11)
lv_rewd = [1, 5, 10, 14, 17, 20, 21, 22, 23, 24, 25]
ev_rewd = [1, 5, 10, 15, 19, 23, 26, 29, 31, 33, 35]

## x軸用リスト、y軸用リスト、x軸表示用リスト、y軸表示用リストの作成
## 元のリストだとスケールが見ずらいため、表示用リストは対数にする
x_list = [0.001*i for i in range(20001)]
y_list = [0.1*i for i in range(101)]
xlog_list = [pow(x, 2)/(20**1) for x in x_list]
ylog_list = [pow(y, 3)/(10**2) for y in y_list]

## 効率最大時のライブボーナス消費量リストの初期化
## xがゼロのときの値は、時間が無限大にある場合のため効率最大時のライブボーナス消費量はゼロ
lv_res_list=[0]
ev_res_list=[0]
tot_res_list=[[0 for i in range(len(y_list))]]

## x軸メインループ
for x in xlog_list[1:]:
    ## 処理進捗通知用
    if(xlog_list.index(x)%5000 == 0): print(x)
    
    ## あるxのときのライブボーナス消費量リストのゼロ埋め初期化
    lv_temp_list=[0 for j in range(11)]
    ev_temp_list=[0 for j in range(11)]
    
    ## ライブボーナス消費量メインループ
    for j in range(11):
        ## ライブ報酬のみ、イベント報酬のみで効率計算
        lv_temp_list[j] = lv_rewd[j] / (lb_list[j] + x)
        ev_temp_list[j] = ev_rewd[j] / (lb_list[j] + x)
    ## 最大効率のライブボーナス消費量を取得
    max_lv = lv_temp_list.index(max(lv_temp_list))
    max_ev = ev_temp_list.index(max(ev_temp_list))

    ## ライブ報酬のみ、イベント報酬のみの最大効率のライブボーナス消費量リストに追加
    lv_res_list.append(max_lv)
    ev_res_list.append(max_ev)
    
    ## あるxのときのトータルライブボーナス消費量リストの初期化
    ## yがゼロの時の値は、ライブ報酬のみの効率最大値になる
    tot_res_temp = [max_lv]

    ## y軸メインループ
    for y in ylog_list[1:]:
        ## あるx、yのときのトータルライブボーナス消費量リストのゼロ埋め初期化
        tot_temp_list=[0 for j in range(11)]
        ## ライブボーナス消費量メインループ
        for j in range(11):
            ## トータルライブボーナス消費量の効率計算
            tot_temp_list[j] = (lv_rewd[j] + ev_rewd[j] * y) / (lb_list[j] + x)
        ## 最大効率のトータルライブボーナス消費量を取得し、トータルライブボーナス消費量リストに追加
        max_tot = tot_temp_list.index(max(tot_temp_list))
        tot_res_temp.append(max_tot)
    ## トータルライブボーナス消費量リストに追加
    tot_res_list.append(tot_res_temp)

## トータルライブボーナス消費量リストのx軸とy軸を反転させるため、*をつける
tot_res_list = list(zip(*tot_res_list))

## デバッグ用表示
for i, y_temp in enumerate(tot_res_list):
    for j, res_temp in enumerate(y_temp):
        ## 典型的でないライブボーナス消費量が格納されていた場合、
        if res_temp not in [0, 2, 3, 5, 7, 10]:
            ## その値とx軸とy軸の感覚値を表示する
            print(res_temp, f'x軸：{x_list[j]:.3f}', f'y軸：{y_list[i]:.1f}')

## グラフ表示のためのリスト作成
colorbar_labels = [i for i in range(11)]
tick_labels = ["0"] + ["" for i in range(1, 10)] + ["大"]

## グラフ作成
## カラーマップは"tab20c"の最初の11色、内挿なし、グラフ外形正方形、最小値0.5、最大値0.5、ゼロ点左下
plt.imshow(tot_res_list, cmap=cm.get_cmap("tab20c", 11), interpolation='none', aspect='auto', vmin=-0.5, vmax=10.5, origin='lower')
plt.title("イベント時\nライブボーナス消費量オススメ")

## x軸のメモリとラベル作成
plt.xticks(ticks=[i*2000 for i in range(11)], labels=tick_labels)
plt.xlabel("時間感覚")
## y軸のメモリとラベル作成
plt.yticks(ticks=[i*10 for i in range(11)], labels=tick_labels)
plt.ylabel("イベント報酬重視率")

## カラーバーの作成
plt.colorbar(ticks=colorbar_labels)

## 同じ階層のフォルダにグラフを保存して表示
plt.savefig("livebonus_rec.png")
plt.show()
