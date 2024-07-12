from kivy.uix.image import AsyncImage
from dep.cover_behavior import CoverBehavior

class CoverImage(CoverBehavior, AsyncImage):

    def __init__(self, **kwargs):
        super(CoverImage, self).__init__(**kwargs)
        texture = self._coreimage.texture
        self.reference_size = texture.size
        self.texture = texture