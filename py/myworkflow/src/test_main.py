from main import Task, Result



def test_run_task() -> None:
    # arrange
    def handler(hello: str) -> Result:
        print(hello)
        return Result(True, None)
    task = Task(handler)
    # act
    result = task.run("Hello, World")
    # assert
    assert result == Result(True, None)

