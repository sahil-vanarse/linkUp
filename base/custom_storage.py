from cloudinary_storage.storage import RawMediaCloudinaryStorage

class CustomCloudinaryStorage(RawMediaCloudinaryStorage):
    def get_valid_name(self, name):
        # Ensure the media/avatars path is preserved
        if not name.startswith('media/'):
            name = f'media/{name}'
        return super().get_valid_name(name)