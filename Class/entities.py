# -*- coding: utf-8 -*-

class WebPage:
    # ポケモン徹底攻略のURL（ベース）
    TETTEIKOURYAKU = "https://yakkun.com/sm/zukan/"
    # ポケモン徹底攻略のURL（フシギダネ）
    TETTEIKOURYAKU_BULBASAUR = "https://yakkun.com/sm/zukan/n1"
    # ポケモン徹底攻略のURL（ズガドーン）
    TETTEIKOURYAKU_BLACEPHALON = "https://yakkun.com/sm/zukan/n806"
    # ポケモン徹底攻略のURL（技一覧）
    TETTEIKOURYAKU_WAZA = "https://yakkun.com/sm/move_list.htm"
    # ポケモン徹底攻略のURL（道具一覧）
    TETTEIKOURYAKU_ITEM = "https://yakkun.com/sm/item_list.htm"
    # ポケモン徹底攻略のアイコンURL
    TETTEIKOURYAKU_ICON = "http://img.yakkun.com/poke/sm_icon/"
    # serebii.netのURL
    SEREBIINET = "https://www.serebii.net/pokedex-sm/"
    # serebii.netのURL（フシギダネ）
    SEREBIINET_BULBASAUR = "https://www.serebii.net/pokedex-sm/001.shtml"
    # pokemon wikiのURL
    POKEMON_WIKI = "http://pokemon.wikia.com/wiki/"
    # pokemon wikiのトップ画像を保存するディレクトリ
    WIKI_TOP_DIRECTORY = "/Users/KitKatBar/Developer/Pokemon/images/WikiTop/"
    # ポケモン徹底攻略の小さいアイコンを保存するディレクトリ
    TETTEIKOURYAKU_ICON_DIRECTORY = "/Users/KitKatBar/Developer/Pokemon/images/YakkunMini/"
    # Pokemon Global Link(PGL)のURL
    PGL = "http://www.pokemon-gl.com"
    # PGLのレーティングバトル画面URL
    PGL_RATING_BATTLE = "https://3ds.pokemon-gl.com/battle/usum/"

class Dao:
    # connection情報
    ACCOUNT = {
        "db": "POKEMON_USUM",
        "host": "localhost",
        "user": "root",
        "passwd": "BJ_Street53"
    }
    
    # 日本語英語対応
class Convert:
    # タイプ、日本語→英語
    TYPE_DICTIONARY_E = {"ノーマル":"NORMAL", "かくとう":"FIGHTING", "ひこう":"FLYING", "どく":"POISON", "じめん":"GROUND", "いわ":"ROCK", "むし":"BUG", "ゴースト":"GHOST", "はがね":"STEEL", "ほのお":"FIRE", "みず":"WATER", "くさ":"GRASS", "でんき":"ELECTRIC", "エスパー":"PSYCHIC", "こおり":"ICE", "ドラゴン":"DRAGON", "あく":"DARK", "フェアリー":"FAIRY"}
    # タイプ、英語→日本語
    TYPE_DICTIONARY_J = {"NORMAL":"ノーマル", "FIGHTING":"かくとう", "FLYING":"ひこう", "どく":"POISON", "GROUND":"じめん", "ROCK":"いわ", "BUG":"むし", "GHOST":"ゴースト", "STEEL":"はがね", "FIRE":"ほのお", "WATER":"みず", "GRASS":"くさ", "ELECTRIC":"でんき", "PSYCHIC":"エスパー", "ICE":"こおり", "DRAGON":"ドラゴン", "DARK":"あく", "FAIRY":"フェアリー"}