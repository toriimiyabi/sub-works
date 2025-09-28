import typer

app = typer.Typer(help="VRP Starter CLI (Day1). まだ中身は空です。")

@app.command()
def hello(name: str = "world"):
    """
    動作確認用のコマンド。
    例: python src/app.py hello --name=you
    """
    typer.echo(f"Hello, {name}! VRP starter is ready.")

@app.command()
def info():
    """
    プロジェクトの説明を表示します。
    """
    typer.echo("VRP Starter: data/ にCSV、outputs/に結果を出す予定です。（Day1は箱だけ）")

if __name__ == "__main__":
    app()
