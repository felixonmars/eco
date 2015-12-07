import pytest

from version_control.gumtree_driver import gumtree, EcoTreeDocument as Doc,\
    EcoTreeNode as Node, EcoTreeNodeClass as NodeClass,\
    GumtreeDiffUpdate as DUpdate, GumtreeDiffDelete as DDelete, GumtreeDiffInsert as DInsert,\
    GumtreeDiffMove as DMove


class Test_gumtree:
    def test_same(self):
        A = NodeClass(1, 'A')
        B = NodeClass(2, 'B')
        C = NodeClass(3, 'C')
        with A.node('a', []) as T0, \
                A.node('a', []) as T1:
            assert gumtree(T0, T1) == []
        with A.node('a', [B.node('b', [])]) as T0, \
                A.node('a', [B.node('b', [])]) as T1:
            assert gumtree(T0, T1) == []
        with A.node('a', [B.node('b', []), C.node('c', [])]) as T0, \
                A.node('a', [B.node('b', []), C.node('c', [])]) as T1:
            assert gumtree(T0, T1) == []

    def test_update(self):
        A = NodeClass(1, 'A')
        B = NodeClass(2, 'B')
        C = NodeClass(3, 'C')
        with A.node('a', [B.node('b', [])]) as T0, \
                A.node('a', [B.node('x', [])]) as T1:
            assert gumtree(T0, T1) == [DUpdate(None, T0[0], 'x')]

    #
    # def test_replace(self):
    #     assert diff3(['b'], ['a'], ['a']) == [Diff3ConflictRegion(base=['b'], derived_main=['a'])]
    #     assert diff3(['b'], ['a'], ['a'], True) == ['a']
    #     assert diff3(['a'], ['b'], ['a']) == ['b']
    #     assert diff3(['a'], ['a'], ['b']) == ['b']
    #     assert diff3(['a', 'b'], ['c', 'b'], ['c', 'b']) == [Diff3ConflictRegion(base=['a'], derived_main=['c']), 'b']
    #     assert diff3(['a', 'b'], ['c', 'b'], ['c', 'b'], True) == ['c', 'b']
    #     assert diff3(['c', 'b'], ['a', 'b'], ['c', 'b']) == ['a', 'b']
    #     assert diff3(['c', 'b'], ['c', 'b'], ['a', 'b']) == ['a', 'b']
    #     assert diff3(['a'], ['b'], ['c']) == [Diff3ConflictRegion(base=['a'], derived_local=['b'], derived_main=['c'])]
    #
    #     assert diff3(['a', 'b', 'c'], ['a', 'b', 'c'], ['a', 'b', 'c']) == ['a', 'b', 'c']
    #     assert diff3(['a', 'b', 'c'], ['a', 'd', 'c'], ['a', 'b', 'c']) == ['a', 'd', 'c']
    #     assert diff3(['a', 'b', 'c'], ['a', 'b', 'c'], ['a', 'd', 'c']) == ['a', 'd', 'c']
    #     assert diff3(['a', 'b', 'c'], ['a', 'e', 'c'], ['a', 'd', 'c']) == ['a', Diff3ConflictRegion(base=['b'], derived_local=['e'], derived_main=['d']), 'c']
    #     assert diff3(['a', 'b', 'c'], ['a', 'b', 'e', 'c'], ['a', 'x', 'c']) == ['a', Diff3ConflictRegion(base=['b'], derived_local=['b', 'e'], derived_main=['x']), 'c']
    #
    # def test_insert(self):
    #     assert diff3(['x', 'a', 'b'], ['a', 'b'], ['a', 'b']) == [Diff3ConflictRegion(base=['x'], derived_main=[]), 'a', 'b']
    #     assert diff3(['x', 'a', 'b'], ['a', 'b'], ['a', 'b'], True) == ['a', 'b']
    #     assert diff3(['a', 'b'], ['x', 'a', 'b'], ['a', 'b']) == ['x', 'a', 'b']
    #     assert diff3(['a', 'b'], ['a', 'b'], ['x', 'a', 'b']) == ['x', 'a', 'b']
    #     assert diff3(['a', 'x', 'b'], ['a', 'b'], ['a', 'b']) == ['a', Diff3ConflictRegion(base=['x'], derived_main=[]), 'b']
    #     assert diff3(['a', 'x', 'b'], ['a', 'b'], ['a', 'b'], True) == ['a', 'b']
    #     assert diff3(['a', 'b'], ['a', 'x', 'b'], ['a', 'b']) == ['a', 'x', 'b']
    #     assert diff3(['a', 'b'], ['a', 'b'], ['a', 'x', 'b']) == ['a', 'x', 'b']
    #     assert diff3(['a', 'b', 'x'], ['a', 'b'], ['a', 'b']) == ['a', 'b', Diff3ConflictRegion(base=['x'], derived_main=[])]
    #     assert diff3(['a', 'b', 'x'], ['a', 'b'], ['a', 'b'], True) == ['a', 'b']
    #     assert diff3(['a', 'b'], ['a', 'b', 'x'], ['a', 'b']) == ['a', 'b', 'x']
    #     assert diff3(['a', 'b'], ['a', 'b'], ['a', 'b', 'x']) == ['a', 'b', 'x']
    #     assert diff3(['a', 'b'], ['a', 'b', 'x'], ['a', 'b', 'c']) == ['a', 'b', Diff3ConflictRegion(base=[], derived_local=['x'], derived_main=['c'])]
    #
    # def test_remove(self):
    #     assert diff3(['a', 'b'], ['x', 'a', 'b'], ['x', 'a', 'b']) == [Diff3ConflictRegion(base=[], derived_main=['x']), 'a', 'b']
    #     assert diff3(['a', 'b'], ['x', 'a', 'b'], ['x', 'a', 'b'], True) == ['x', 'a', 'b']
    #     assert diff3(['x', 'a', 'b'], ['a', 'b'], ['x', 'a', 'b']) == ['a', 'b']
    #     assert diff3(['x', 'a', 'b'], ['x', 'a', 'b'], ['a', 'b']) == ['a', 'b']
    #     assert diff3(['a', 'b'], ['a', 'x', 'b'], ['a', 'x', 'b']) == ['a', Diff3ConflictRegion(base=[], derived_main=['x']), 'b']
    #     assert diff3(['a', 'b'], ['a', 'x', 'b'], ['a', 'x', 'b'], True) == ['a', 'x', 'b']
    #     assert diff3(['a', 'x', 'b'], ['a', 'b'], ['a', 'x', 'b']) == ['a', 'b']
    #     assert diff3(['a', 'x', 'b'], ['a', 'x', 'b'], ['a', 'b']) == ['a', 'b']
    #     assert diff3(['a', 'b'], ['a', 'b', 'x'], ['a', 'b', 'x']) == ['a', 'b', Diff3ConflictRegion(base=[], derived_main=['x'])]
    #     assert diff3(['a', 'b'], ['a', 'b', 'x'], ['a', 'b', 'x'], True) == ['a', 'b', 'x']
    #     assert diff3(['a', 'b', 'x'], ['a', 'b'], ['a', 'b', 'x']) == ['a', 'b']
    #     assert diff3(['a', 'b', 'x'], ['a', 'b', 'x'], ['a', 'b']) == ['a', 'b']
    #     assert diff3(['a', 'b', 'x'], ['a', 'b'], ['a', 'b', 'c']) == ['a', 'b', Diff3ConflictRegion(base=['x'], derived_main=['c'], derived_local=[])]
    #     assert diff3(['a', 'b', 'x'], ['a', 'b', 'c'], ['a', 'b']) == ['a', 'b', Diff3ConflictRegion(base=['x'], derived_main=[], derived_local=['c'])]
    #
