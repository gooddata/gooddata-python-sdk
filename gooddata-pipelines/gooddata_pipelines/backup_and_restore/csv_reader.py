# (C) 2025 GoodData Corporation

import csv
from typing import Iterator


class CSVReader:
    """Class to read the input CSV file and return its content as a list of strings."""

    @staticmethod
    def read_backup_csv(file_path: str) -> list[str]:
        """Reads the input CSV file, validates its structure, and returns its
        content as a list of strings.
        """

        with open(file_path) as csv_file:
            reader: Iterator[list[str]] = csv.reader(
                csv_file, skipinitialspace=True
            )

            try:
                # Skip the header
                headers = next(reader)

                if len(headers) > 1:
                    raise ValueError(
                        "Input file contains more than one column. Please check the input and try again."
                    )

            except StopIteration:
                # Raise an error if the iterator is empty
                raise ValueError("No content found in the CSV file.")

            # Read the content
            content = [row[0] for row in reader]

            # If the content is empty (no rows), raise an error
            if not content:
                raise ValueError("No workspaces found in the CSV file.")

        return content
