import os
import csv

from .driver import Driver


class DuplicateNameError(Exception):
    pass


def save_content(url, fw):
    fw.write('this is a line')
    fw.write('this is another line')

class Refresh:

    def __init__(self, csvfp):
        self.names = set()
        self.errors = []
        self.build(csvfp)

    def build(self, csvfp):
        "read in the given csv and build the files containing the expected data"

        if not os.path.exists(csvfp):
            raise IOError('File {} does not exist'.format(csvfp))

        csv_dir = os.path.dirname(os.path.abspath(csvfp))
        self.expected_dir = os.path.join(csv_dir,'expected')
        if not os.path.isdir(self.expected_dir):
            os.makedirs(self.expected_dir)

        with open(csvfp) as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    self.build_expecteds(row)
                except DuplicateNameError as err:
                    self.errors.append(err)


    def build_expecteds(self, row):
        """build file in the subdirector named "expected "
        """

        url, name = row
        url = url.strip()
        name = name.strip()

        # check that this name has  not bee used earlier in the file
        if name in self.names:
            raise DuplicateNameError(name)

        self.names.add(name)

        fn = os.path.join(self.expected_dir, name)
        with open(fn, 'w') as fw:
            save_content(url, fw)


