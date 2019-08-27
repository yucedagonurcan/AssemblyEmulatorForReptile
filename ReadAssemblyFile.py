import csv


class AssemblyReader():
    def __init__(self, assembly_filename, instruction_list):
        self.assembly_filename = assembly_filename
        self.data_dict = {}
        self.csv_rows = []
        self.code_rows = []
        self.label_dict = {}
        self.data_memory = []
        self.instruction_list = instruction_list
        self.ReadAssembly()
        self.AssemblyParser()

    def ReadAssembly(self):
        with open(self.assembly_filename, "r") as csv_file:
            raw_lines = csv_file.readlines()
            self.csv_line_counter = 0
            for row in raw_lines:
                if not any(row.strip()):
                    continue

                row = " ".join(row.strip().split("//")[0].split())
                self.csv_line_counter += 1
                self.csv_rows.append(row)

    def AssemblyParser(self):
        is_data_reading = None
        data_memory_cursor = 0

        for line_idx in range(self.csv_line_counter):
            current_line = self.csv_rows[line_idx]
            if (current_line == ".code"):
                is_data_reading = False

            elif (current_line == ".data"):
                is_data_reading = True
            else:
                if is_data_reading:
                    assert ":" in current_line, f"You need to include ':' to the variable ends in '.data' section.\nLine {line_idx}: '{current_line}'"
                    row_key, row_value = current_line.split(":")
                    row_value = row_value.strip()
                    try:
                        if row_value == '':
                            self.data_dict[row_key] = data_memory_cursor
                            self.data_memory.append(0)
                            data_memory_cursor += 1

                        elif row_value[:2] == "0x":
                            if row_value[2:] == "":
                                raise Exception(
                                    f"Wrong type of hex representation: {row_value}.\nLine: {line_idx}: {current_line}")
                            self.data_dict[row_key] = data_memory_cursor
                            self.data_memory.append(int(
                                row_value, 16))
                            data_memory_cursor += 1

                        elif row_value.split()[0] == ".space":

                            self.data_dict[row_key] = data_memory_cursor
                            [self.data_memory.append(0) for _ in range(int(
                                row_value.split()[1]))]
                            data_memory_cursor += int(
                                row_value.split()[1])

                        else:
                            self.data_dict[row_key] = data_memory_cursor
                            self.data_memory.append(int(row_value))
                            data_memory_cursor += 1

                    except ValueError:
                        raise Exception(
                            f"Storing non-integer value to a variable-> {current_line} in Line:{line_idx + 1}")
                elif is_data_reading is False:
                    words_line = current_line.split()
                    if len(words_line) == 0:
                        continue
                    if words_line[0] not in self.instruction_list:
                        self.label_dict[words_line[0]] = len(
                            self.code_rows)
                        self.code_rows.append(" ".join(words_line[1:]))
                    else:
                        self.code_rows.append(" ".join(words_line))

                else:
                    raise Exception(
                        f"Line: {line_idx+1} needs to be one of the following:\n\t1).code\n\t2).data\n")
        del self.csv_rows
