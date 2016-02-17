import os
import shutil
import json

from .compare import Structure, get_content_from_url


class DuplicateNameError(Exception):
    pass


class Refresh(Structure):

    def __init__(self, csvfp):
        super(Refresh, self).__init__(csvfp)
        self.names = set()

    def run(self):
        "read in the given csv and build the files containing the expected data"

        # clear down the directory and recreate empty
        shutil.rmtree(self.expected_dir, ignore_errors=True)
        os.makedirs(self.expected_dir)

        next_row_data = self.next_row()  # generator which gives the url and row

        for url, name in next_row_data:
                try:
                    self.build_expecteds(url, name)
                except DuplicateNameError as err:
                    self.errors.append(err)


    def build_expecteds(self, url, name):
        """build file in the subdirector named "expected... "
        """

        # check that this name has  not bee used earlier in the file
        if name in self.names:
            raise DuplicateNameError(name)

        self.names.add(name)

        content = get_content_from_url(url)
        self.save_content(json.dumps(content), name)

    def save_content(self, content, name):
        fn = os.path.join(self.expected_dir, name)
        with open(fn, 'w') as fw:
            fw.write(content)



