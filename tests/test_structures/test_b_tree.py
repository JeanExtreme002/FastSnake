from fastsnake.structures.b_tree import *


b_tree = BTree(2)


def test_b_tree_insert():
    b_tree.insert((100,))
    b_tree.insert((35,))
    b_tree.insert((65,))
    b_tree.insert((130,))
    b_tree.insert((180,))

    assert b_tree.root.keys[0][0] == 65
    assert b_tree.root.child[0].keys[0][0] == 35
    assert b_tree.root.child[1].keys[0][0] == 100
    assert b_tree.root.child[1].keys[1][0] == 130
    assert b_tree.root.child[1].keys[2][0] == 180

    b_tree.insert((10,))
    b_tree.insert((20,))

    assert b_tree.root.child[0].keys[0][0] == 10
    assert b_tree.root.child[0].keys[1][0] == 20
    assert b_tree.root.child[0].keys[2][0] == 35

    b_tree.insert((40,))

    assert b_tree.root.keys[0][0] == 20
    assert b_tree.root.keys[1][0] == 65

    assert b_tree.root.child[0].keys[0][0] == 10
    assert b_tree.root.child[1].keys[0][0] == 35
    assert b_tree.root.child[1].keys[1][0] == 40

    b_tree.insert((50,))
    b_tree.insert((70,))
    b_tree.insert((80,))
    b_tree.insert((90,))
    b_tree.insert((140,))
    b_tree.insert((110,))
    b_tree.insert((120,))
    b_tree.insert((160,))
    b_tree.insert((190,))
    b_tree.insert((260,))
    b_tree.insert((240,))

    # Level 0
    assert b_tree.root.keys[0][0] == 65
    assert b_tree.root.keys[1][0] == 100

    # Level 1
    assert b_tree.root.child[0].keys[0][0] == 20
    assert b_tree.root.child[1].keys[0][0] == 80
    assert b_tree.root.child[2].keys[0][0] == 130
    assert b_tree.root.child[2].keys[1][0] == 160
    assert b_tree.root.child[2].keys[2][0] == 190

    # Level 2
    assert b_tree.root.child[0].child[0].keys[0][0] == 10
    assert b_tree.root.child[1].child[0].keys[0][0] == 70
    assert b_tree.root.child[2].child[0].keys[0][0] == 110
    assert b_tree.root.child[2].child[0].keys[1][0] == 120
    assert b_tree.root.child[2].child[1].keys[0][0] == 140
    assert b_tree.root.child[2].child[2].keys[0][0] == 180
    assert b_tree.root.child[2].child[3].keys[0][0] == 240
    assert b_tree.root.child[2].child[3].keys[1][0] == 260


def test_b_tree_search():
    assert b_tree.search(65) == (b_tree.root, 0)
    assert b_tree.search(100) == (b_tree.root, 1)
    assert b_tree.search(20) == (b_tree.root.child[0], 0)
    assert b_tree.search(80) == (b_tree.root.child[1], 0)
    assert b_tree.search(130) == (b_tree.root.child[2], 0)
    assert b_tree.search(160) == (b_tree.root.child[2], 1)
    assert b_tree.search(190) == (b_tree.root.child[2], 2)
    assert b_tree.search(10) == (b_tree.root.child[0].child[0], 0)
    assert b_tree.search(70) == (b_tree.root.child[1].child[0], 0)
    assert b_tree.search(110) == (b_tree.root.child[2].child[0], 0)
    assert b_tree.search(120) == (b_tree.root.child[2].child[0], 1)
    assert b_tree.search(140) == (b_tree.root.child[2].child[1], 0)
    assert b_tree.search(180) == (b_tree.root.child[2].child[2], 0)
    assert b_tree.search(240) == (b_tree.root.child[2].child[3], 0)
    assert b_tree.search(260) == (b_tree.root.child[2].child[3], 1)

    assert b_tree.search(0) is None
    assert b_tree.search(65 - 1) is None
    assert b_tree.search(65 + 1) is None
    assert b_tree.search(100 - 1) is None
    assert b_tree.search(100 + 1) is None
    assert b_tree.search(20 - 1) is None
    assert b_tree.search(20 + 1) is None
    assert b_tree.search(80 - 1) is None
    assert b_tree.search(80 + 1) is None
    assert b_tree.search(130 - 1) is None
    assert b_tree.search(130 + 1) is None
    assert b_tree.search(160 - 1) is None
    assert b_tree.search(160 + 1) is None
    assert b_tree.search(140 - 1) is None
    assert b_tree.search(140 + 1) is None
    assert b_tree.search(240 - 1) is None
    assert b_tree.search(240 + 1) is None
    assert b_tree.search(260 - 1) is None
    assert b_tree.search(260 + 1) is None
    assert b_tree.search(10 - 1) is None
    assert b_tree.search(10 + 1) is None
