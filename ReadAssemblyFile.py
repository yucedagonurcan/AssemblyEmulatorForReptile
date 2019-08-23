import csv


class AssemblyReader():
    def __init__(self, assembly_filename, instruction_list):
        self.assembly_filename = assembly_filename
        self.data_dict = {}
        self.csv_rows = []
        self.code_rows = []
        self.label_dict = {}
        self.instruction_list = instruction_list
        self.ReadAssembly()
        self.AssemblyParser()

    def ReadAssembly(self):
        with open(self.assembly_filename) as csv_file:
            csv_reader = csv.reader(csv_file)
            self.csv_line_counter = 0
            for row in csv_reader:
                row = " ".join(row[0].strip().split("//")[0].split())
                self.csv_line_counter += 1
                self.csv_rows.append(row)

    def AssemblyParser(self):
        is_data_reading = None
        for line_idx in range(self.csv_line_counter):
            current_line = self.csv_rows[line_idx]
            if (current_line == ".code"):
                is_data_reading = False

            elif (current_line == ".data"):
                is_data_reading = True
            else:
                if is_data_reading:
                    row_key, row_value = current_line.split(":")
                    try:
                        self.data_dict[row_key] = 0 if row_value == '' else int(
                            row_value.strip())
                    except ValueError:
                        raise Exception(
                            f"Storing non-integer value to a variable-> {current_line} in Line:{line_idx + 1}")
                elif is_data_reading is False:
                    words_line = current_line.split()
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
