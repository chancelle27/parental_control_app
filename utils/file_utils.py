class FileUtils:
    @staticmethod
    def read_file(file_path):
        with open(file_path, "r") as file:
            return file.readlines()

    @staticmethod
    def write_file(file_path, data):
        with open(file_path, "w") as file:
            file.writelines(data)
