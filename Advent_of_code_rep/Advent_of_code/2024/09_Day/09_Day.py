class DiskCompactor:
    _free_space = "."
    _expanded_disk_map = None

    def __init__(self, disk_map, free_space="."):
        self._expanded_disk_map = self._expand(disk_map)
        self._free_space = free_space

    def compacted_checksum(self, allow_fragmented_files=True):
        return self._checksum(
            self._compact()
            if allow_fragmented_files
            else self._compact_without_fragmentation()
        )

    def _expand(self, disk_map):
        return [
            item
            for pair in [
                [str(ii // 2) for _ in range(int(disk_map[ii]))]
                + (
                    [self._free_space for _ in range(int(disk_map[ii + 1]))]
                    if ii + 1 < len(disk_map)
                    else []
                )
                for ii in range(0, len(disk_map), 2)
            ]
            for item in pair
        ]

    def _compact(self):
        disk = self._expanded_disk_map.copy()
        for ii, block in enumerate(disk[::-1]):
            if block == self._free_space:
                continue
            block_index = len(disk) - 1 - ii
            free_index = disk.index(self._free_space)
            if free_index >= block_index:
                break
            disk = self._transfer(disk, block_index, free_index)
        return disk

    def _compact_without_fragmentation(self):
        disk = self._expanded_disk_map.copy()
        current, current_count = -1, 0
        for ii, num in enumerate(disk[::-1]):
            if num == self._free_space:
                if current != -1:
                    disk = self._transfer_file_to_free_space(
                        disk, len(disk) - ii, current_count
                    )
                    current, current_count = -1, 0
            elif current == -1:
                current, current_count = num, 1
            elif num == current:
                current_count += 1
            elif num != current:
                disk = self._transfer_file_to_free_space(
                    disk, len(disk) - ii, current_count
                )
                current, current_count = num, 1
            else:
                raise Exception("Unexpected condition")
        return disk

    def _transfer_file_to_free_space(self, disk, transfer_start, count):
        free_space_start = self._find_free_space(disk, count, transfer_start)
        if free_space_start == -1:
            return disk
        return self._transfer(disk, transfer_start, free_space_start, count)

    def _transfer(self, disk, start, to, count=1):
        for ii in range(count):
            disk[to + ii] = disk[start + ii]
            disk[start + ii] = self._free_space
        return disk

    def _find_free_space(self, disk, size, file_index, start=0):
        """recursive"""
        try:
            first_free_space = disk.index(self._free_space, start, file_index)
        except ValueError:
            return -1
        for ii in range(first_free_space + 1, first_free_space + size):
            if ii >= file_index:
                return -1
            if disk[ii] != self._free_space:
                return self._find_free_space(disk, size, file_index, start=ii)
        return first_free_space

    def _checksum(self, disk):
        return sum(
            [
                ii * int(block)
                for ii, block in enumerate(disk)
                if block != self._free_space
            ]
        )


def get_lines(test=False):
    with open(("test" if test else "input") + ".txt") as file:
        for ln in file:
            yield ln.strip()


if __name__ == "__main__":
    compactor = DiskCompactor("".join(get_lines()))
    print("1:", compactor.compacted_checksum())
    print("2:", compactor.compacted_checksum(allow_fragmented_files=False))