from typing import Optional
from threading import Lock

class MemoryBlock:
    def __init__(self, start: int, size: int):
        """Initialize a memory block with start index and size.
        Args:
            start (int): Start index of the block in memory.
            size (int): Size of the block.
        """
        
        self.start = start 
        self.size = size 
        self.data = [''] * size 
        
    def __str__(self):
        """String representation of the MemoryBlock."""
        return f"<Block start={self.start} size={self.size} data={self.data}>"

class MemoryManager:
    def __init__(self, size: int):
        """Initialize the memory manager with a given size. 
        Args:
            size (int): Size of the memory to manage.
        """
        if size <= 0:
            raise ValueError("Memory size must be positive.")
        self.size = size
        self.memory = ['-'] * size 
        self.allocations = {}       
        self.next_id = 1        
        self.lock = Lock()      

    def alloc(self, size: int) -> Optional[int]:
        """Allocate a block of memory of the given size."""
        with self.lock:
            if size <= 0 or size > len(self.memory):
                raise ValueError("Invalid size for allocation.")
            i = 0
            while i <= len(self.memory) - size:
                if all(self.memory[j] == '-' for j in range(i, i + size)):
                    for j in range(i, i + size):
                        self.memory[j] = 'X'
                    block_id = self.next_id
                    self.next_id += 1
                    self.allocations[block_id] = MemoryBlock(i, size)
                    return block_id
                i += 1
            # If no contiguous space is found, raise an exception
            raise MemoryError("Insufficient contiguous memory. Consider defragmenting.")


    def free(self, block_id: int) -> bool:
        """Free the allocated block with the given block_id."""
        with self.lock:
            if block_id not in self.allocations:
                raise ValueError(f"Block ID {block_id} does not exist.")
            # Free the block
            block = self.allocations.pop(block_id, None)
            if not block:
                return False
            for i in range(block.start, block.start + block.size):
                self.memory[i] = '-'
            return True

    def defragment(self) -> None:
        """Defragment the memory to compact all allocated blocks."""
        with self.lock:
            new_memory = ['-'] * len(self.memory)
            new_allocations = {}
            curr = 0

            # Sort blocks by their original start position to preserve order
            for block_id, block in sorted(self.allocations.items(), key=lambda kv: kv[1].start):
                # Move block to the new position
                for i in range(block.size):
                    new_memory[curr + i] = 'X'
                new_allocations[block_id] = MemoryBlock(curr, block.size)
                new_allocations[block_id].data = block.data[:]  # Copy block data
                curr += block.size

            # Update memory and allocations
            self.memory = new_memory
            self.allocations = new_allocations
    def write(self, block_id: int, offset: int, data: str) -> None:
        """Write data to the allocated block at the given offset."""
        with self.lock:
            # Validate inputs
            block = self.allocations.get(block_id)
            if not block:
                raise ValueError(f"Block ID {block_id} does not exist.")
            if offset < 0 or offset >= block.size:
                raise IndexError(f"Offset {offset} is out of bounds for block {block_id}.")
            if len(data) > block.size - offset:
                raise ValueError(f"Data exceeds block size. Available space: {block.size - offset}.")
            
            # Write data to the block
            for i, char in enumerate(data):
                block.data[offset + i] = char

    def read(self, block_id: int, offset: int, length: int) -> str:
        """Read data from the allocated block at the given offset."""
        with self.lock:
            # Validate inputs
            if block_id not in self.allocations:
                raise ValueError(f"Block ID {block_id} does not exist.")
            if offset < 0:
                raise IndexError("Offset cannot be negative.")
            if length <= 0:
                raise ValueError("Length must be positive.")
            if offset >= len(self.memory):
                raise IndexError("Offset exceeds memory size.")
            if offset + length > len(self.memory):
                raise IndexError("Read range exceeds memory size.")
            block = self.allocations.get(block_id)
            if not block:
                raise ValueError(f"Block ID {block_id} does not exist.")
            if offset < 0 or offset + length > block.size:
                raise IndexError(f"Read range is out of bounds for block {block_id}.")
            
            # Read data from the block
            return ''.join(block.data[offset:offset + length])
        
    def __str__(self):
        """
        String representation of the MemoryManager.
        Shows the current state of memory and allocations.
        """
        with self.lock:
            result = ['-'] * len(self.memory)
            for block in self.allocations.values():
                for i in range(block.size):
                    char = block.data[i]
                    result[block.start + i] = char if char else 'X'
            return ''.join(result)
        
        
# Example usage
if __name__ == "__main__":
    # Initialize memory manager with size 5
    mem_manager = MemoryManager(5)
    print("Initial memory:", mem_manager)

    # Allocate 5 blocks of size 1 each
    block1 = mem_manager.alloc(1)  # Block ID 1
    block2 = mem_manager.alloc(1)  # Block ID 2
    block3 = mem_manager.alloc(1)  # Block ID 3
    block4 = mem_manager.alloc(1)  # Block ID 4
    block5 = mem_manager.alloc(1)  # Block ID 5
    print(f"Allocated blocks: {block1}, {block2}, {block3}, {block4}, {block5}")
    print("Memory after allocations:", mem_manager)
  
    # free block 2nd and 4th
    mem_manager.free(block2)
    mem_manager.free(block4)
    print(f"Freed blocks {block2} and {block4}: {mem_manager}") 
    # Try to allocate a block of size 2 (should fail and require defragmentation)
    try:
        block6 = mem_manager.alloc(2)  # Block ID 6
        print(f"Allocated block {block6}: {mem_manager}")
    except MemoryError as e:
        print(f"Allocation failed: {e}")
        print("Defragmenting memory...")
        mem_manager.defragment()
        print("Memory after defragmentation:", mem_manager)

        # Retry allocation after defragmentation
        block6 = mem_manager.alloc(2)  # Block ID 6
        print(f"Allocated block {block6}: {mem_manager}")

    # write data to block 1
    mem_manager.write(block1, 0, "A")
    print(f"Written data to block {block1}: {mem_manager}")
    # read data from block 1
    data = mem_manager.read(block1, 0, 1)
    print(f"Read from block {block1}: {data}") 
    
    
