'''
@date 20131124
@author: mjbommar
'''

# Standard imports
import unittest

# Import PD space
import pd.space

class SpaceTest(unittest.TestCase):

    def testInit(self):
        space = pd.space.Lattice2D(4, 4)
        self.assertIsNotNone(space)

        
    def testPut(self):
        # Create space
        space = pd.space.Lattice2D(4, 4)
        
        # Simple put
        put_return = space.put((1,1), "StringX")
        self.assertTrue(put_return)


    def testPut2(self):
        # Create space
        space = pd.space.Lattice2D(4, 4)
        
        # Overput put
        space.put((1,1), "String1")
        put_return = space.put((1,1), "String2")
        self.assertFalse(put_return)
        
    def testVonNeumann(self):
        # Create space
        space2 = pd.space.Lattice2D(4, 4)
        
        # Setup space
        for i in range(4):
            for j in range(4):
                cell_value = "String ({0},{1})".format(i, j)
                space2.put((i, j), cell_value)
        
        neighbors = space2.get_neighbors_von_neumann((2,2), 2)
        expected_neighbors = ['String (0,2)', 'String (1,1)', 'String (1,2)', 'String (1,3)', 'String (2,0)', 'String (2,1)', 'String (2,3)', 'String (3,1)', 'String (3,2)', 'String (3,3)']
        self.assertEqual(neighbors, expected_neighbors)
                     


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()