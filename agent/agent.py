"""作業を自動でこなすAIエージェント（Windows / Python）

使い方:
    pip install anthropic
    set ANTHROPIC_API_KEY=sk-ant-...      (PowerShell なら $env:ANTHROPIC_API_KEY="sk-ant-...")
    python agent.py                        (作業フォルダは ./workspace)
    python agent.py C:\\Users\\me\\Documents\\作業   (作業フォルダを指定)

できること:
    - 作業フォルダ内のファイル一覧・読み込み・書き込み
    - PowerShell コマンドの実行（実行前に必ず確認）
    - Web検索・Webページの取得（Anthropic のサーバー側で実行）
"""

import subprocess
import sys
from pathlib import Path

import anthropic
from anthropic import beta_tool

# 使うAIモデル。
#   "claude-haiku-5-5" … 最安（Opusの約1/40）。普段使いはこれで十分
#   "claude-opus-5-5"  … 最高性能。難しい仕事で品質が足りないときに
MODEL = "claude-haiku-5-5"
WORKSPACE = Path(sys.argv[1] if len(sys.argv) > 1 else "workspace").resolve()

SYSTEM_PROMPT = f"""あなたはユーザーのWindows PC上で作業を代行するAIエージェントです。
作業フォルダ: {WORKSPACE}
- ファイル操作はこの作業フォルダの中だけで行えます。パスは作業フォルダからの相対パスで指定してください。
- 必要に応じてツールを組み合わせ、依頼を最後までやり遂げてください。
- コマンド実行やファイル書き込みはユーザーの承認が必要です。拒否されたら別の方法を考えるか、理由を説明してください。
- 回答は日本語で、簡潔にまとめてください。"""


def _resolve(path: str) -> Path:
    """作業フォルダの外を指すパスを拒否する。"""
    target = (WORKSPACE / path).resolve()
    if not target.is_relative_to(WORKSPACE):
        raise ValueError(f"作業フォルダの外にはアクセスできません: {path}")
    return target


def _confirm(message: str) -> bool:
    answer = input(f"\n⚠️  {message}\n   実行してよいですか？ [y/N] ").strip().lower()
    return answer in ("y", "yes")


@beta_tool
def list_files(path: str = ".") -> str:
    """作業フォルダ内のファイルとフォルダの一覧を返す。

    Args:
        path: 一覧を表示するフォルダ（作業フォルダからの相対パス）。
    """
    try:
        target = _resolve(path)
        entries = sorted(target.iterdir(), key=lambda p: (p.is_file(), p.name))
        lines = [f"{'[DIR] ' if p.is_dir() else '      '}{p.name}" for p in entries]
        return "\n".join(lines) or "(空のフォルダです)"
    except Exception as e:
        return f"エラー: {e}"


@beta_tool
def read_file(path: str) -> str:
    """テキストファイルの中身を読む。

    Args:
        path: 読むファイル（作業フォルダからの相対パス）。
    """
    try:
        return _resolve(path).read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"エラー: {e}"


@beta_tool
def write_file(path: str, content: str) -> str:
    """テキストファイルを作成または上書きする。必要なフォルダは自動で作られる。

    Args:
        path: 書き込むファイル（作業フォルダからの相対パス）。
        content: ファイルに書き込む内容全体。
    """
    try:
        target = _resolve(path)
        action = "上書き" if target.exists() else "新規作成"
        if not _confirm(f"ファイルを{action}します: {target}（{len(content)}文字）"):
            return "ユーザーが書き込みを拒否しました。"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"{action}しました: {path}"
    except Exception as e:
        return f"エラー: {e}"


@beta_tool
def run_command(command: str) -> str:
    """作業フォルダで PowerShell コマンドを実行し、出力を返す（タイムアウト120秒）。

    Args:
        command: 実行する PowerShell コマンド。
    """
    if not _confirm(f"コマンドを実行します:\n   {command}"):
        return "ユーザーがコマンドの実行を拒否しました。"
    shell = ["powershell", "-NoProfile", "-Command", command] if sys.platform == "win32" else ["bash", "-c", command]
    try:
        result = subprocess.run(
            shell, cwd=WORKSPACE, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=120,
        )
        output = (result.stdout + result.stderr).strip()
        return f"終了コード {result.returncode}\n{output[-20000:] or '(出力なし)'}"
    except subprocess.TimeoutExpired:
        return "エラー: 120秒以内に終わらなかったため中断しました。"
    except Exception as e:
        return f"エラー: {e}"


TOOLS = [
    list_files,
    read_file,
    write_file,
    run_command,
]


def web_tools(model: str) -> list:
    """Web検索・Web取得ツール（Anthropic 側で実行されるので実装は不要）。モデルに合う版を選ぶ。"""
    if "haiku" in model:
        return [
            {"type": "web_search_20250305", "name": "web_search", "max_uses": 5},
            {"type": "web_fetch_20250910", "name": "web_fetch", "max_uses": 5},
        ]
    return [
        {"type": "web_search_20260209", "name": "web_search", "max_uses": 5},
        {"type": "web_fetch_20260209", "name": "web_fetch", "max_uses": 5},
    ]


TOOLS += web_tools(MODEL)


def print_reply(message, speaker: str = "🤖") -> None:
    for block in message.content:
        if block.type == "text" and block.text.strip():
            print(f"\n{speaker} {block.text}")
        elif block.type == "tool_use":
            print(f"   🔧 {block.name} を使用中...")
        elif block.type == "server_tool_use":
            print(f"   🌐 {block.name} を使用中...")


def run_turn(
    client: anthropic.Anthropic,
    messages: list,
    system: str = SYSTEM_PROMPT,
    tools: list = TOOLS,
    speaker: str = "🤖",
    model: str = MODEL,
) -> str:
    """1回の依頼を、Claude がツールを使い終わるまで実行する。messages は会話履歴として更新される。

    戻り値は最後の回答のテキスト。
    """
    extra = {}
    if "haiku" not in model:
        # 安全フィルタで断られたときに、自動で別モデルに切り替えて回答させる（Haiku は非対応）
        extra = {"betas": ["server-side-fallback-2026-07-01"], "fallbacks": "default"}
    for _ in range(5):  # pause_turn（長いWeb検索の一時停止）からの再開は5回まで
        runner = client.beta.messages.tool_runner(
            model=model,
            max_tokens=16000,
            system=system,
            tools=tools,
            messages=messages,
            output_config={"effort": "high"},
            **extra,
        )
        last = None
        for message in runner:
            last = message
            print_reply(message, speaker)
            messages.append({"role": "assistant", "content": message.content})
            tool_response = runner.generate_tool_call_response()
            if tool_response is not None:
                messages.append(tool_response)

        if last is None or last.stop_reason != "pause_turn":
            if last is not None and last.stop_reason == "refusal":
                print(f"\n{speaker} （この依頼には対応できませんでした）")
                return "（この依頼には対応できませんでした）"
            if last is not None and last.stop_reason == "max_tokens":
                print(f"\n{speaker} （回答が長すぎて途中で切れました。「続けて」と送ってください）")
            if last is None:
                return ""
            return "\n".join(b.text for b in last.content if b.type == "text")
    return "（Web検索が長引いたため途中で止まりました）"


def main() -> None:
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    client = anthropic.Anthropic()  # 環境変数 ANTHROPIC_API_KEY を使う
    messages: list = []

    print(f"AIエージェント起動（作業フォルダ: {WORKSPACE}）")
    print("依頼を入力してください。終了は exit、会話リセットは reset。")

    while True:
        try:
            user_input = input("\n👤 > ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            break
        if user_input.lower() == "reset":
            messages.clear()
            print("会話をリセットしました。")
            continue

        checkpoint = len(messages)  # エラー時はこの依頼の前まで会話を巻き戻す
        messages.append({"role": "user", "content": user_input})
        try:
            run_turn(client, messages)
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

    print("終了します。")


if __name__ == "__main__":
    main()
