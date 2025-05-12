import unittest
from main import MemoryManager, MemoryBlock


class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        """Set up a MemoryManager instance for testing."""
        self.mem_manager = MemoryManager(5)

    def test_initial_memory(self):
        """Test the initial state of memory."""
        self.assertEqual(str(self.mem_manager), "-----")

    def test_alloc_success(self):
        """Test successful memory allocation."""
        block_id = self.mem_manager.alloc(3) 
        self.assertIsNotNone(block_id)
        self.assertEqual(str(self.mem_manager), "XXX--")

    def test_alloc_full_memory(self):
        """Test allocating the entire memory."""
        block_id = self.mem_manager.alloc(5)
        self.assertIsNotNone(block_id)
        self.assertEqual(str(self.mem_manager), "XXXXX")

    def test_alloc_insufficient_space(self):
        """Test allocation when there is insufficient space."""
        self.mem_manager.alloc(3) # Allocate 3 blocks: XXX--
        with self.assertRaises(MemoryError):
            self.mem_manager.alloc(3) # Attempt to allocate 3 more blocks

    def test_alloc_invalid_size(self):
        """Test allocation with invalid sizes."""
        with self.assertRaises(ValueError):
            self.mem_manager.alloc(0) # Invalid size
        with self.assertRaises(ValueError):
            self.mem_manager.alloc(-1) # Invalid size
        with self.assertRaises(ValueError):
            self.mem_manager.alloc(6) # Invalid size (exceeds memory)
  
    def test_free_success(self):
        """Test freeing a memory block."""
        block_id = self.mem_manager.alloc(3)
        self.mem_manager.free(block_id)
        self.assertEqual(str(self.mem_manager), "-----")

    def test_free_invalid_block(self):
        """Test freeing an invalid block ID."""
        with self.assertRaises(ValueError):
            self.mem_manager.free(999)

    def test_free_already_freed_block(self):
        """Test freeing a block that has already been freed."""
        block_id = self.mem_manager.alloc(3)
        self.mem_manager.free(block_id)
        with self.assertRaises(ValueError):
            self.mem_manager.free(block_id)

    def test_write_success(self):
        """Test writing data to a memory block."""
        block_id = self.mem_manager.alloc(3)
        self.mem_manager.write(block_id, 0, "abc")
        block = self.mem_manager.allocations[block_id]
        self.assertEqual(block.data, list("abc"))

    def test_write_out_of_bounds(self):
        """Test writing data that exceeds block size."""
        block_id = self.mem_manager.alloc(3)
        with self.assertRaises(ValueError):
            self.mem_manager.write(block_id, 0, "abcdef")

    def test_write_invalid_block(self):
        """Test writing to an invalid block ID."""
        with self.assertRaises(ValueError):
            self.mem_manager.write(999, 0, "data")

    def test_read_success(self):
        """Test reading data from a memory block."""
        block_id = self.mem_manager.alloc(3)
        self.mem_manager.write(block_id, 0, "abc")
        data = self.mem_manager.read(block_id, 0, 3)
        self.assertEqual(data, "abc")

    def test_read_out_of_bounds(self):
        """Test reading data that exceeds block size."""
        block_id = self.mem_manager.alloc(3)
        self.mem_manager.write(block_id, 0, "abc")
        with self.assertRaises(IndexError):
            self.mem_manager.read(block_id, 0, 5)

    def test_read_invalid_block(self):
        """Test reading from an invalid block ID."""
        with self.assertRaises(ValueError):
            self.mem_manager.read(999, 0, 3)

    def test_alloc_fragmentation_error(self):
        """Test allocation failure due to fragmentation."""
        block1 = self.mem_manager.alloc(1)
        block2 = self.mem_manager.alloc(1)
        block3 = self.mem_manager.alloc(1)
        block4 = self.mem_manager.alloc(1)
        block5 = self.mem_manager.alloc(1)
        self.mem_manager.free(block2)
        self.mem_manager.free(block4)
        with self.assertRaises(MemoryError):
            self.mem_manager.alloc(2)

    def test_defragment_preserves_data(self):
        """Test that defragmentation preserves block data."""
        block1 = self.mem_manager.alloc(2)
        block2 = self.mem_manager.alloc(2)
        self.mem_manager.write(block2, 0, "cd")  # Write data to block2
        self.mem_manager.free(block1)  # Free block1
        self.mem_manager.defragment()  # Defragment memory
        block = self.mem_manager.allocations[block2]
        self.assertEqual(block.data, list("cd"))  # Verify block2's data is preserved

    def test_alloc_after_defragment(self):
        """Test allocation after defragmentation."""
        block1 = self.mem_manager.alloc(2)
        block2 = self.mem_manager.alloc(2)
        self.mem_manager.free(block1)
        self.mem_manager.defragment()
        block3 = self.mem_manager.alloc(3)
        self.assertIsNotNone(block3)
        self.assertEqual(str(self.mem_manager), "XXX--")

   
    def test_alloc_after_defragment(self):
        """Test allocation after defragmentation."""
        block1 = self.mem_manager.alloc(2)  # Allocate block1 (XX---)
        block2 = self.mem_manager.alloc(2)  # Allocate block2 (XXXX-)
        self.mem_manager.free(block1)       # Free block1 (--XX-)
        self.mem_manager.defragment()       # Defragment memory (XX---)
        block3 = self.mem_manager.alloc(3)  # Allocate block3 (XXXXX)
        self.assertIsNotNone(block3)
        self.assertEqual(str(self.mem_manager), "XXXXX")

if __name__ == "__main__":
    unittest.main()