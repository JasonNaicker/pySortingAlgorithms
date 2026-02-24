from __future__ import annotations
from typing import Optional

class Heap:
    """
    A binary heap implementation supporting both min-heap and max-heap behavior.

    Attributes:
        _arr (list[int]): Internal array representing the heap.
        _is_min_heap (bool): If True, heap behaves as a min-heap; otherwise, as a max-heap.
    """

    def __init__(self, arr: list[int], isMinHeap: bool = False) -> None:
        """
        Initialize a Heap from an existing list of integers.

        Args:
            arr (list[int]): Initial elements to store in the heap.
            isMinHeap (bool): Whether the heap is a min-heap (default False = max-heap).
        """
        self._arr = list(arr)
        self._is_min_heap = isMinHeap
        self.build_heap()

    # Helpers
    def _left(self, index: int) -> int:
        """
        Return the index of the left child of a node.

        Args:
            index (int): Parent node index.

        Returns:
            int: Left child index.
        """
        return (index * 2) + 1

    def _right(self, index: int) -> int:
        """
        Return the index of the right child of a node.

        Args:
            index (int): Parent node index.

        Returns:
            int: Right child index.
        """
        return (index * 2) + 2

    def _parent(self, index: int) -> int:
        """
        Return the index of the parent of a node.

        Args:
            index (int): Child node index.

        Returns:
            int: Parent node index.
        """
        return (index - 1) // 2

    def _swap(self, a: int, b: int) -> None:
        """
        Swap two elements in the heap array.

        Args:
            a (int): Index of the first element.
            b (int): Index of the second element.
        """
        self._arr[a], self._arr[b] = self._arr[b], self._arr[a]

    def _compare(self, a: int, b: int) -> bool:
        """
        Compare two elements in the heap based on heap type.

        Args:
            a (int): Index of the first element.
            b (int): Index of the second element.

        Returns:
            bool: True if element at index a has higher priority than element at index b.
        """
        return self._arr[a] < self._arr[b] if self._is_min_heap else self._arr[a] > self._arr[b]

    @property
    def size(self) -> int:
        """
        Return the number of elements in the heap.

        Returns:
            int: Heap size.
        """
        return len(self._arr)

    def is_empty(self) -> bool:
        """
        Check whether the heap is empty.

        Returns:
            bool: True if the heap is empty, False otherwise.
        """
        return len(self._arr) == 0

    def heapify_down(self, index: int, size: int) -> None:
        """
        Restore the heap property by moving an element downwards.

        Args:
            index (int): Starting index for heapification.
            size (int): Number of elements to consider in the heap.
        """
        cumulative: int = index
        left: int = self._left(index)
        right: int = self._right(index)

        if left < size and self._compare(left, cumulative):
            cumulative = left

        if right < size and self._compare(right, cumulative):
            cumulative = right

        if cumulative != index:
            self._swap(index, cumulative)
            self.heapify_down(cumulative, size)

    def heapify_up(self, index: int) -> None:
        """
        Restore the heap property by moving an element upwards.

        Args:
            index (int): Starting index for heapification.
        """
        while index > 0:
            parent = self._parent(index)
            if self._compare(index, parent):
                self._swap(index, parent)
                index = parent
            else:
                break

    def build_heap(self) -> None:
        """
        Convert the internal array into a valid heap.
        """
        start_index: int = (self.size // 2) - 1

        for i in range(start_index, -1, -1):
            self.heapify_down(i, self.size)

    def peek(self) -> Optional[int]:
        """
        Return the top element of the heap without removing it.

        Returns:
            Optional[int]: Root element of the heap, or None if empty.
        """
        return None if self.is_empty else self._arr[0]

    def push(self, value: int) -> None:
        """
        Insert a new value into the heap.

        Args:
            value (int): Value to insert.
        """
        self._arr.append(value)
        self.heapify_up(len(self._arr) - 1)

    def pop(self) -> int:
        """
        Remove and return the root element of the heap.

        Returns:
            int: The root value.

        Raises:
            IndexError: If the heap is empty.
        """
        if self.is_empty():
            raise IndexError("Pop from empty heap")

        root = self._arr[0]
        lastIndex = self.size - 1

        self._swap(0, lastIndex)
        self._arr.pop()

        if not self.is_empty():
            self.heapify_down(0, self.size)
        return root

    def push_pop(self, value: int) -> int:
        """
        Push a value onto the heap and then pop and return the root.

        This operation is more efficient than calling push() followed by pop().

        Args:
            value (int): Value to push.

        Returns:
            int: The popped value.
        """
        if self.is_empty():
            self.push(value)
            return value

        root = self._arr[0]

        if (self._is_min_heap and value > root) or not (self._is_min_heap and value < root):
            self._arr[0] = value
            self.heapify_down(0, self.size)
            return root
        else:
            return value

    def replace(self, oldValue: int, newValue: int) -> None:
        """
        Replace an existing value in the heap with a new value.

        Args:
            oldValue (int): Value to replace.
            newValue (int): New value to insert.

        Raises:
            ValueError: If the heap is empty or the value is not found.
        """
        if self.is_empty():
            raise ValueError("Heap is empty")

        try:
            index = self._arr.index(oldValue)
        except ValueError:
            raise ValueError(f"{oldValue} not found in heap")

        self._arr[index] = newValue
        parent = self._parent(index)

        if index > 0 and self._compare(index, parent):
            self.heapify_up(index)
        else:
            self.heapify_down(index, self.size)

    def clear(self) -> None:
        """
        Remove all elements from the heap.
        """
        self._arr.clear()

    def display_contents(self) -> None:
        """
        Display the heap in a tree-like level-by-level format.
        """
        if self.is_empty():
            print("Empty Heap")
            return

        print("[MinHeap]:" if self._is_min_heap else "[MaxHeap]:")

        n: int = self.size
        level: int = 0
        index: int = 0

        while index < n:
            level_size = 2 ** level
            level_nodes = self._arr[index: index + level_size]

            indent = " " * (2 ** (max(0, (self.size.bit_length() - level - 1))))
            spacing = " " * (2 ** (max(0, (self.size.bit_length() - level))))

            print(indent + spacing.join(str(v) for v in level_nodes))

            index += level_size
            level += 1

    def print_contents(self) -> None:
        """
        Print the raw internal array representing the heap.
        """
        if self.is_empty():
            print("Empty tree")
            return

        print("[MinHeap]:" if self._is_min_heap else "[MaxHeap]:")
        print(self._arr)

    def __repr__(self) -> str:
        """
        Return a string representation of the heap.
        """
        heap_type = "MinHeap" if self._is_min_heap else "MaxHeap"
        return f"[{heap_type}] {self._arr}"

    def __len__(self) -> int:
        """
        Return the number of elements in the heap.
        """
        return self.size

    def __bool__(self) -> bool:
        """
        Return True if the heap is not empty.
        """
        return not self.is_empty()

    def items(self) -> list[int]:
        """
        Return a shallow copy of the heap elements.

        Returns:
            list[int]: Heap contents.
        """
        return self._arr.copy()
