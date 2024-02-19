from src.main import render_hello_template


def test_render_hello_template():
    params = {"name": "World"}
    result = render_hello_template(params)

    assert result == "Hello World"
