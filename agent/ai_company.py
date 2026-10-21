"""AI社員チーム（Windows / Python）

あなたが社長として指示を出すと、リーダー（AI部長）が仕事を分解して
部署ごとのAI社員に振り分け、結果をまとめて報告します。

    社長（あなた）
      └ AI部長 ……… 仕事を分解して振り分け、結果をまとめる
          ├ 事務担当 …… Excel/CSV集計、報告書・議事録・メール文面、ファイル整理
          ├ リサーチ担当 … Web調査、競合・市場・商品の比較レポート
          ├ 広報担当 …… SNS投稿、ブログ記事、商品説明、営業メール
          └ 経理担当 …… 売上・経費の集計、請求書・見積書、月次の収支レポート

使い方:
    pip install anthropic
    $env:ANTHROPIC_API_KEY="sk-ant-..."
    python ai_company.py                    (作業フォルダは ./workspace)
    python ai_company.py C:\\作業フォルダ

初回起動時に作業フォルダへ「会社情報.md」が作られます。会社名・事業内容・
文体のルールなどを書いておくと、全員がそれを前提に仕事をします。
"""

import anthropic
from anthropic import beta_tool

from agent import WORKSPACE, list_files, read_file, run_command, run_turn, web_tools, write_file

# 使うAIモデル。"claude-haiku-5-5" が最安、"claude-opus-5-5" が最高性能。
# 品質が足りないときは、まず部長だけ Opus にすると費用を抑えつつ仕事の段取りが良くなる
LEADER_MODEL = "claude-haiku-5-5"
EMPLOYEE_MODEL = "claude-haiku-5-5"

COMPANY_FILE = WORKSPACE / "会社情報.md"
COMPANY_TEMPLATE = """# 会社情報
（AI社員全員がこの内容を前提に仕事をします。自由に書き換えてください。書き換えたら再起動してください）

## 会社名・事業内容
- 会社名:
- 事業内容:
- 主な商品・サービス:
- お客様（ターゲット）:

## 仕事のルール
- 文体: です・ます調
- 成果物は「成果物」フォルダに保存する
"""

WEB_SEARCH, WEB_FETCH = web_tools(EMPLOYEE_MODEL)

EMPLOYEES = {
    "事務担当": {
        "icon": "📋",
        "role": "事務担当。Excel/CSVの集計、報告書・議事録・メール文面の作成、ファイル整理が得意です。"
                "データの集計にはPowerShellやPythonのコマンドを使えます。",
        "tools": [list_files, read_file, write_file, run_command],
    },
    "リサーチ担当": {
        "icon": "🔎",
        "role": "リサーチ担当。Webで競合・市場・商品などを調べ、出典URL付きの分かりやすいレポートにまとめます。"
                "事実と推測ははっきり分けて書きます。",
        "tools": [list_files, read_file, write_file, WEB_SEARCH, WEB_FETCH],
    },
    "広報担当": {
        "icon": "📣",
        "role": "広報担当。SNS投稿文、ブログ記事、商品説明、営業メールを書きます。"
                "お客様に伝わる言葉選びを大切にし、必要なら複数案を出します。",
        "tools": [list_files, read_file, write_file, WEB_SEARCH],
    },
    "経理担当": {
        "icon": "💰",
        "role": "経理担当。売上・経費の集計、請求書・見積書の作成、月次の収支レポートを担当します。"
                "金額の計算は暗算せず、必ずPythonやPowerShellのコマンドで計算して検算します。"
                "税金や会計処理の判断が必要な点は、税理士への確認が必要と明記します。",
        "tools": [list_files, read_file, write_file, run_command],
    },
}


def load_company_info() -> str:
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    if not COMPANY_FILE.exists():
        COMPANY_FILE.write_text(COMPANY_TEMPLATE, encoding="utf-8")
    return COMPANY_FILE.read_text(encoding="utf-8")


COMPANY_INFO = load_company_info()


def employee_prompt(name: str) -> str:
    return f"""あなたはこの会社で働くAI社員の「{name}」です。
{EMPLOYEES[name]["role"]}

AI部長から仕事を受け取り、自分で最後までやり遂げてください。
- 作業フォルダ: {WORKSPACE}（ファイル操作はこの中だけ。パスは相対パスで指定）
- 成果物はファイルに保存し、最後に「何をしたか・保存したファイル名・注意点」を短く報告してください。
- 情報が足りないときは、妥当な仮定を置いて進め、その仮定を報告に書いてください。
- 日本語で仕事をしてください。

{COMPANY_INFO}"""


LEADER_PROMPT = f"""あなたはこの会社のAI部長です。社長（ユーザー）の指示を受けて、部下のAI社員に仕事を振り分けます。

部下:
{chr(10).join(f"- {name}: {e['role']}" for name, e in EMPLOYEES.items())}

進め方:
- 社長の指示を担当ごとの具体的な仕事に分け、assign_task で依頼してください。依頼文には目的・必要な情報・成果物の形式を書いてください。
- 前の担当の結果を次の担当に渡す場合（例: リサーチ結果をもとに広報が記事を書く）は、順番に依頼してください。
- 簡単な質問には、部下に振らずに自分で答えて構いません。
- 全員の仕事が終わったら、社長に向けて結果を簡潔に報告してください（何ができたか、保存したファイル、確認してほしい点）。
- 作業フォルダ: {WORKSPACE}

{COMPANY_INFO}"""

client = anthropic.Anthropic()  # 環境変数 ANTHROPIC_API_KEY を使う
# 社員ごとの会話履歴。同じ社員には前の仕事の続きを頼める（reset で全員分を消す）
employee_histories: dict[str, list] = {name: [] for name in EMPLOYEES}


@beta_tool
def assign_task(employee: str, task: str) -> str:
    """部下のAI社員に仕事を依頼し、その社員の報告を受け取る。

    Args:
        employee: 依頼する社員。「事務担当」「リサーチ担当」「広報担当」「経理担当」のいずれか。
        task: 依頼内容。目的・必要な情報・成果物の形式を具体的に書く。
    """
    if employee not in EMPLOYEES:
        return f"エラー: 「{employee}」という社員はいません。{'、'.join(EMPLOYEES)} から選んでください。"
    e = EMPLOYEES[employee]
    print(f"\n   ➡️  {employee}に依頼: {task[:80]}{'…' if len(task) > 80 else ''}")
    history = employee_histories[employee]
    checkpoint = len(history)
    history.append({"role": "user", "content": task})
    try:
        report = run_turn(
            client, history, employee_prompt(employee), e["tools"], f"{e['icon']} {employee}:", EMPLOYEE_MODEL
        )
    except anthropic.APIError as err:
        del history[checkpoint:]
        return f"エラー: {employee}の作業中に問題が起きました（{err}）"
    except BaseException:  # Ctrl+C など。中途半端な履歴を残さない
        del history[checkpoint:]
        raise
    return report or "（報告がありませんでした）"


LEADER_TOOLS = [list_files, read_file, assign_task]


def main() -> None:
    print(f"🏢 AI社員チーム出社しました（作業フォルダ: {WORKSPACE}）")
    print(f"   メンバー: AI部長、{'、'.join(EMPLOYEES)}")
    print(f"   会社情報: {COMPANY_FILE}")
    print("社長、指示をどうぞ。終了は exit、全員の記憶をリセットは reset。")

    messages: list = []
    while True:
        try:
            user_input = input("\n👤 社長 > ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            break
        if user_input.lower() == "reset":
            messages.clear()
            for history in employee_histories.values():
                history.clear()
            print("全員の会話をリセットしました。")
            continue

        checkpoint = len(messages)  # エラー時はこの指示の前まで会話を巻き戻す
        messages.append({"role": "user", "content": user_input})
        try:
            run_turn(client, messages, LEADER_PROMPT, LEADER_TOOLS, "👔 AI部長:", LEADER_MODEL)
        except anthropic.AuthenticationError:
            print("❌ APIキーが正しくありません。ANTHROPIC_API_KEY を確認してください。")
            del messages[checkpoint:]
        except anthropic.RateLimitError:
            print("❌ 利用制限に達しました。少し待ってから再度お試しください。")
            del messages[checkpoint:]
        except anthropic.APIStatusError as e:
            print(f"❌ APIエラー ({e.status_code}): {e.message}")
            del messages[checkpoint:]
        except anthropic.APIConnectionError:
            print("❌ ネットワークに接続できません。")
            del messages[checkpoint:]
        except KeyboardInterrupt:
            print("\n（中断しました）")
            del messages[checkpoint:]

    print("本日の業務を終了します。お疲れさまでした。")


if __name__ == "__main__":
    main()
