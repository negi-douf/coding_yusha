from argparse import ArgumentParser

from coding_yusha.controller.game_master import GameMaster

if __name__ == "__main__":
    parser = ArgumentParser(description="coding_yushaの実行ファイルです")
    parser.add_argument("stage", type=str, help="ステージ名")
    parser.add_argument("allies", type=str, nargs="+", help="味方ユニットのファイルパス")
    args = parser.parse_args()

    _ = GameMaster(args.stage, *args.allies)
