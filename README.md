# Shogi-DiscordBot : Discord上での将棋を実装
##  概要
Discord上で将棋の対局をするためのコードです。先後交互にコマンドを使用して対局することができます。
使用するには、shogi.pyに示してある部分にご自身のBOTトークンとサーバーIDを入力する必要があります。
不足しているライブラリ等をインストールしたのち、ご自身の環境で動かすと使用できます。

## 使い方
### `/taikyoku` ー ルール説明を表示し、盤面を初期化する
![taikyoku.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/2825387/26263573-7823-3e33-a46a-88e4fb41861f.png)
### `/sasu <指し手>` ー 指し手の指示に従い、コマを動かす(下で説明)
![sasu.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/2825387/1dc8e443-f170-6411-b0e5-75e18fd2b9cc.png)

指し手の入力にはCSA形式というものを用いています。簡単に説明すると、

|  | 歩兵 | 香車 | 桂馬 | 銀将 | 金将 | 角行 | 飛車 | 王将 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 生駒 | FU | KY | KE | GI | KI | KE | GI | OU |
| 成駒 | TO | NY | NK | NG |  | UM | RY |  |

この表の記号(/taikyokuコマンド使用時にも表示)と、数字２桁（駒台は00）の位置情報を組み合わせて

`＜動かす前の位置＞＋＜動かした後の位置＞＋＜動かした後の駒の記号＞`

で入力します。これだけだと「なるほどわからん」となると思うので例を挙げると、

`76歩 → /sasu 7776FU`

`77`→動かす前の位置

`76`→動かす後の位置

`FU`→歩

となります。あと変則的な手を2つ紹介します。

`52銀打 → /sasu 0052GI`(駒台は00)

`23飛車成 → /sasu 2823RY`(移動後の駒で表す)

## 注意点
私の能力不足と終盤の「とりあえずうごいたらええねん」精神により、コードは**西夏文字並みの読みにくさ**となっております。
