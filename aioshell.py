import asyncio
from asyncio.subprocess import PIPE, STDOUT


class Result:
    def __init__(self, status, stdout, stderr):
        self.status = status
        self._stdout = stdout or ""
        self._stderr = stderr or ""
        if stdout is not None:
            self.stdout = stdout.decode("utf-8")
        else:
            self.stdout = None
        if stderr is not None:
            self.stderr = stderr.decode("utf-8")
        else:
            self.stderr = None

    def __repr__(self):
        return f"<Result status={self.status} stdout={len(self._stdout)} stderr={len(self._stderr)}>"


async def run(shell_command):
    p = await asyncio.create_subprocess_shell(
        shell_command, stdin=PIPE, stdout=PIPE, stderr=STDOUT
    )
    stdout, stderr = await p.communicate()
    code = p.returncode
    return Result(code, stdout, stderr)


if __name__ == "__main__":

    async def test():
        r = await run("pwd")
        print(r.stdout, r.stderr, r.status)

    import sys

    if sys.platform.startswith("win"):
        loop = (
            asyncio.ProactorEventLoop()
        )  # subprocess pipes only works with this under Win
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
