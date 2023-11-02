import typer


def main(api_token: str, vcs: str = "github"):
    print(vcs)

if __name__=="__main__":
    typer.run(main)