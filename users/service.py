from posts.models import Post


class PostObjectsService:
    base_model = Post

    # def __init__(self):
        

    def get_post(self, id) -> Post:
        post = Post.objects.get(id=id)

        return post