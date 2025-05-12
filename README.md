# Virtual Memory Manager

## Overview
This project is a simple **Memory Manager** that simulates memory allocation, freeing, and defragmentation. It allows you to allocate memory blocks, free them, write data to blocks, read data from blocks, and compact memory when needed.

---

## Design Choices

### Data Structures
- **Memory**: Represented as a list where `'-'` indicates free space and `'X'` indicates allocated space.
- **Blocks**: Each allocated block is tracked using a `MemoryBlock` object, which stores:
  - `start`: Starting index of the block.
  - `size`: Size of the block.
  - `data`: Data stored in the block.
- **Allocations**: A dictionary maps block IDs to their corresponding `MemoryBlock` objects.

### Thread Safety
- A `threading.Lock` ensures that memory operations (e.g., allocation, freeing, writing, reading, defragmentation) are thread-safe.

### Error Handling
- **`ValueError`**: Raised for invalid block IDs or sizes.
- **`IndexError`**: Raised for out-of-bounds memory access.
- **`MemoryError`**: Raised when there is insufficient contiguous memory for allocation.

---

## How It Works

### Key Features
1. **Allocate Memory**: Finds the first available contiguous space for a block of the requested size.
2. **Free Memory**: Marks a block as free and removes its metadata.
3. **Write Data**: Writes data to a specific block at a given offset.
4. **Read Data**: Reads data from a specific block starting at a given offset.
5. **Defragment Memory**: Moves allocated blocks to the beginning of memory to create larger contiguous free spaces.

### Algorithms
- **Allocation**: Scans memory linearly to find free space.
- **Defragmentation**: Moves allocated blocks to the start of memory while preserving their order and data.

---

## Trade-offs

1. **Simplicity**: The implementation is straightforward but not optimized for large memory sizes.
2. **Performance**: Linear scans for allocation and full defragmentation can be slow for large memory.
3. **Thread Safety**: A single lock ensures safety but may reduce performance in multithreaded environments.

---

## Future Improvements

1. **Faster Allocation**: Use a free list or buddy allocation system to improve performance.
2. **Incremental Defragmentation**: Spread defragmentation over multiple operations to avoid blocking.
3. **Better Concurrency**: Replace the global lock with more granular locks for better multithreaded performance.
4. **Visualization**: Add tools to visualize memory usage and fragmentation.
5. **Testing**: Add stress tests and multithreaded scenarios to ensure robustness.

---

## Conclusion
This project provides a basic memory manager with essential features. While it works well for small-scale use cases, there is room for optimization and scalability improvements.