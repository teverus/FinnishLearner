class Table:
    def __init__(
        self,
        rows: list,
        rows_centered: bool = False,
        headers: list = (),
        headers_centered: bool = False,
        headers_upper: bool = False,
        border_headers_top: str = "-",
        border_rows_top: str = "-",
        border_rows_bottom: str = "-",
        table_width: int = 0,
        table_title: str = "",
        table_title_upper: bool = True,
        table_title_centered: bool = True,
        show_index: bool = True,
        column_border: str = "|",
        custom_index: dict = None,
        index_column_width: dict = None
    ):
        # === Given values
        # Rows
        self.rows = self.convert_rows(rows)
        self.rows_centered = rows_centered
        self.rows_border_top = border_rows_top
        self.rows_border_bottom = border_rows_bottom

        # Headers
        self.headers = [headers]
        self.headers_centered = headers_centered
        self.headers_top_border = border_headers_top
        self.headers_upper = headers_upper

        # Table
        self.table_title = table_title
        self.table_title_upper = table_title_upper
        self.table_title_centered = table_title_centered
        self.width_total = table_width
        self.show_index = show_index
        self.column_wall = column_border
        self.custom_index = custom_index
        self.available_options = []

        # === Calculated values
        self.walls = 0
        self.inner_padding = 0
        self.extra = 0
        self.widths_max = {}
        self.width_to_be_covered = 0
        self.widths_target = 0
        self.width_index = self.get_proper_index_column_width(index_column_width)

        self.table = []

        # === Preparing the table
        self.force_string_type_on_the_data()
        self.perform_width_analysis()
        self.calculate_paddings()
        self.calculate_columns()

        # === Printing the table
        self.print_the_table()

    def get_proper_index_column_width(self, index_column_width):
        indices = [len(str(len(self.rows)))]

        if self.custom_index:
            indices.append(max([len(str(i)) for i in self.custom_index.values()]))

        if index_column_width:
            indices.append(index_column_width)

        return max(indices)

    @staticmethod
    def convert_rows(rows):
        converted_rows = [e if isinstance(e, list) else [e] for e in rows]

        max_columns_number = max([len(element) for element in converted_rows])
        for row in converted_rows:
            diff = max_columns_number - len(row)
            if diff:
                for _ in range(diff):
                    row.append("")

        return converted_rows

    def force_string_type_on_the_data(self):
        for row in self.rows:
            for index, line in enumerate(row):
                row[index] = str(line)

    def perform_width_analysis(self):
        column_number = len(self.rows[0])
        column_number = column_number + 1 if self.show_index else column_number

        self.widths_max = {index: 0 for index, _ in enumerate(self.rows[0])}
        for row in self.headers + self.rows:
            for index, column in enumerate(row):
                if self.widths_max[index] < len(column):
                    self.widths_max[index] = len(column)

        if self.show_index:
            self.widths_max[-1] = self.width_index

        self.walls = column_number - 1
        self.inner_padding = column_number * 2

        self.extra = self.walls + self.inner_padding
        self.width_to_be_covered = sum(self.widths_max.values()) + self.extra
        if not self.width_total:
            self.width_total = self.width_to_be_covered

    def calculate_paddings(self):
        if self.width_to_be_covered > self.width_total:
            while self.width_to_be_covered != self.width_total:
                self.adjust_widths(decrease=True)

        elif self.width_to_be_covered < self.width_total:
            while self.width_to_be_covered != self.width_total:
                self.adjust_widths(increase=True)

    def adjust_widths(self, increase=False, decrease=False):
        if increase:
            value = min([v for k, v in self.widths_max.items() if k != -1])
        elif decrease:
            value = max(self.widths_max.values())
        else:
            raise Exception("[ERROR] You must choose either minimum or maximum")

        index = max([k for k, v in self.widths_max.items() if k != -1 and v == value])

        if increase:
            self.widths_max[index] += 1
        elif decrease:
            self.widths_max[index] -= 1
        else:
            raise Exception("[ERROR] You must choose either minimum or maximum")

        self.width_to_be_covered = sum(self.widths_max.values()) + self.extra

    def calculate_columns(self):
        for element in (self.headers, self.rows):
            self.create_columns(element)

    def create_columns(self, some_list):
        for index_row, row in enumerate(some_list):
            for index_col, column in enumerate(row):
                column_width = len(column)
                target_width = self.widths_max[index_col]

                if column_width > target_width:
                    tail = column[-3:]
                    head = column[: (target_width - len(tail) - 1)]
                    column = f"{head}~{tail}"

                is_header = [row] == self.headers
                centered = self.headers_centered if is_header else self.rows_centered
                align = column.center if centered else column.ljust

                row[index_col] = align(target_width, " ")
                if is_header and self.headers_upper:
                    row[index_col] = row[index_col].upper()

            if self.custom_index and row[0].strip() in self.custom_index.keys():
                proper_index = str(self.custom_index[row[0].strip()])
            else:
                proper_index = str(index_row + 1)
            index = f" {proper_index.rjust(self.width_index)} {self.column_wall}"
            if [row] != self.headers:
                self.available_options.append(proper_index)

            rows = f" {f' {self.column_wall} '.join(row)} "

            if [row] == self.headers:
                if row:
                    index = index.replace("1", "#")
                    table_head = f"{index}{rows}" if self.show_index else rows
                    self.headers[index_row] = table_head
            else:
                some_list[index_row] = f"{index}{rows}" if self.show_index else rows

    def print_the_table(self):
        headers = self.headers[0]
        headers_top = self.headers_top_border * self.width_total if headers else ""
        table_top = self.get_table_top()
        table_bottom = self.rows_border_bottom * self.width_total

        if self.table_title:
            if self.headers_top_border:
                print(headers_top)
            tt = self.table_title
            tt = tt.upper() if self.table_title_upper else tt
            tt = tt.center(self.width_total) if self.table_title_centered else tt
            print(tt)

        if headers:
            if self.headers_top_border:
                print(headers_top)
            print(headers)
            head_list = [headers_top, headers] if self.headers_top_border else [headers]
            [self.table.append(element) for element in head_list]

        if self.rows_border_top:
            print(table_top)

        [print(row) for row in self.rows]

        if self.rows_border_bottom:
            print(table_bottom)

        [self.table.append(e) for e in [table_top, *self.rows, table_bottom]]

    def get_table_top(self):
        if self.headers == [()]:
            return self.rows_border_top * self.width_total
        else:
            if self.show_index:
                all_but_index = [v for k, v in self.widths_max.items() if k != -1]
                widths = [f"{self.rows_border_top * w}" for w in all_but_index]
                col = ["-" * self.width_index] + widths
            else:
                col = [f"{self.rows_border_top * w}" for w in self.widths_max.values()]
            columns_walls = f"{self.rows_border_top}+{self.rows_border_top}".join(col)
            border_full = f"{self.rows_border_top}{columns_walls}{self.rows_border_top}"
            return border_full
