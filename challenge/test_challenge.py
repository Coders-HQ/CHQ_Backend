target = __import__("challenge")
sum = target.test_func

def test_challenge():
    assert sum()==3,"should be 3"

if __name__ == "__main__":
    test_challenge()