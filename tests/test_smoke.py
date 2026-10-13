from assistant.rules import reply


def test_greeting():
    assert "Hello" in reply("hi")


def test_office_lookup():
    assert "I.101" in reply("Where is the Training Office?")


def test_unknown():
    assert "don't know" in reply("what is the meaning of life")


def test_empty():
    assert reply("   ") == "Please type a question."


def test_help():
    response = reply("help")
    assert "where an office is" in response
    assert "when it opens" in response
    assert "Training Office" in response
    
def test_office_lookup_partial_training():
    response = reply("training")
    assert "Training Office" in response

def test_office_lookup_partial_another_word():
    response = reply("student")
    assert "I don't know that yet" not in response