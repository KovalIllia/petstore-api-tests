import os.path


class FileFactory:

    @staticmethod
    def pet_image(filename: str = "test_dog.jpg") -> str:
        return os.path.join(os.path.dirname(__file__), "resources", filename)
