
def test_utils():
    from ..library.utils import replace_html, is_development, create_id, timestamp

    test_case_html = """this is a string <h1>hello</h1>"""
    print(replace_html(test_case_html))
    assert replace_html(test_case_html) == "hello",  "test case not working correctly"
