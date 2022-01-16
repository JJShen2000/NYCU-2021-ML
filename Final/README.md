# Machine Learning Final Project Report - Predict the Prices of the Mobile
###### tags: `NYCU` `ML`
## I. Introduction
在這個project中，我嘗試建立分類模型來預測手機的等級，而等級是依照價格的高低來分。以下價格皆指市價而不是原價。
### File
- data
    - Raw data: `raw_data/*`, `soc_score.csv`
    - 處理後的data: `sogi_mobile.csv`
- Program
    - scraper: `sogi_mobile_.py`
    - data processing: `data_processing.ipynb`
    - model: `model.ipynb`
## II. Data Collection
- 主要的資料來源是我從[SOGI手機王](https://www.sogi.com.tw/)爬蟲得到的，蒐集台灣目前買的到(不含已下架)的手機，爬下來的原始資料大小為 $208\ rows × 123\ columns$。
    - 補充說明:<br>原本其實是要用[gsmarena](https://www.gsmarena.com/)的資料，雖然資料量較大(光是2020年後且是市占前8品牌的就大概有8xx筆)，但train完後卻效果不好，可能原因是gsm的價格錯誤較多，且貨幣很多種，容易受匯率影響，因此改成用台灣的網站。
- 我對爬下來的資料做了不少處理，以下僅說明較重要的。
    - 處理器: 由於處理器名字本身較難量化，我又參考[Geekbench](https://browser.geekbench.com/android-benchmarks)官網的跑分資料(加上工人智慧查缺漏的)，將SOC轉成CPU單核及多核的跑分。(忽略GPU)
    - 將複合型的資料(像是IEEE 802.11傳輸協議裡有很多子協議)挑出較重要的做one-hot。
    - 缺漏的資料: 
        - 缺太多的資料直接drop。
        - 只缺一些的部分就工人智慧直接查，然後加進去。
- 最後整理出`sogi_mobile.csv`這個檔案，總共有51個columns、201筆資料。<br>以下是所有欄位:
![](https://i.imgur.com/7pq52Qv.png)

## III. Preprocessing
- Feature($X$)
    - 由於前面已經做了大部分的處理，因此在model這裡讀完資料後就只要將$X$中的Brand(品牌)及一些類型是bool的features做one-hot。

- Label($y$)
    - 原始的label單位是新台幣，因此要將它們分類。我原先是想以萬元來分成4類: 中低階(<10k)、中高階(10k ~ 20k)、高階(20k ~ 30k)、旗艦(>30k)，但這樣會imbalance，因為多數都是在20k以下，validation時旗艦的筆數會很少，所以我後來用quantile來分成4類(Top 25%, Top 25-50%, Last 25-50%, Last 25%)。
    - Label的分布<br>![](https://i.imgur.com/EmqviHJ.png)

    - Quantile<br>![](https://i.imgur.com/Vhcc22z.png)

- Some visualization(可以右鍵在新分頁開啟)
    - 處理器多核跑分與價格的關係<br>![](https://i.imgur.com/BCyVPE9.png)

    - 品牌與價格的關係<br>![](https://i.imgur.com/oxpKqHG.png)<br>可以看到Apple確實大部分都是粉紅色(最貴的)，SUGAR手機大多是較低價的。

## IV. Models
經過實驗，我選出這4種model:
- RandomForest(sklearn)
    - max_depth=20, n_estimators=100
- DecisionTree(sklearn)
    - max_depth=8
- xgboost(sklearn api)
    -  n_estimators=200, learning_rate= 0.3, max_depth=10, reg_lambda=1
-  KNN(sklearn)
    -  n_neighbors=5
## V. Results
### Accuracy一覽表(跑10次得出)

| Models | Avg. | Max |  Median | Min |
| ------ | ------------- | ------------- | ------- | --- |
|   Random Forest     |       0.79403        |       0.820896        |    0.793533     |   0.771144  |
|     Decision Tree   |        0.71791      |         0.756219      |    0.716418     |   0.681592  |
|    XGBoost    |     0.778609          |           0.80597    |   0.776119      |  0.746269   |
|    KNN    | 0.695522          | 0.736318          |  0.691542   |  0.666667   |
### Accuracy, Confusion Matrix, Recall, Precision
- RandomForest
    - ![](https://i.imgur.com/8YNidlE.png)

- DecisionTree
    - ![](https://i.imgur.com/rnUGgBk.png)

- xgboost
    - ![](https://i.imgur.com/9EV4J2y.png)

- KNN
    - ![](https://i.imgur.com/qpFxyf5.png)

## VI. Conclusion
- 整體來說，Random Forest $\gt$ XGBoost $>>$ Decision Tree $>$ KNN
- 考慮到資料量不多，我認為model的表現已經不錯了，GSM的資料雖然有800多筆，但Random Forest的accuracy大約只能到$68\%$。
- 觀察各個classifier的confusion matrix可以發現基本上就算判斷錯誤也是在鄰近的class。
- 我嘗試將Brand從feature去除，結果發現accuracy竟然也不差，原先想用SHAP分析看看但一直安裝失敗...
    - ![](https://i.imgur.com/3eS1aVf.png)
### Improvement
因為資料是後來新爬的，有點趕，忘記順便爬發布時間和原價，如果能比較加入原價、時間等的feature是否會比較準確應該也很有趣。
### Application
[假說]在準確度足夠高(能反映手機價值)的情況下或許能讓使用者找到那些被低估的手機，也就是CP值高的手機。
### 加碼
後來也有嘗試用GradientBoostingRegressor來做回歸
![](https://i.imgur.com/RU1lMC7.png)
![](https://i.imgur.com/2OtT8i2.png)
