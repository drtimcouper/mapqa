import os
import csv
import shutil

from .driver import Driver


class DuplicateNameError(Exception):
    pass


def get_content(url):
    pass


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
        csvfp_name = os.path.splitext(os.path.basename(csvfp))[0]

        self.expected_dir = os.path.join(csv_dir,'expected_{}'.format(csvfp_name))
       # clear down the directory and recreate empty
        shutil.rmtree(self.expected_dir, ignore_errors=True)
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

        content = get_content(url)
        self. save_content(content, name)

    def save_content(self, content, name):
        fn = os.path.join(self.expected_dir, name)
        with open(fn, 'w') as fw:
            fw.write(content)



