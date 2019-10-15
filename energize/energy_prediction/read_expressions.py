from energize.pipeline.pipeline import PipelineModule

class ReadExpressions(PipelineModule):

    def __init__(self, next=None):
        super().__init__(next)

    def do_shizzle(self, **kwargs):
        image = kwargs.pop('image', None)
        locations = kwargs.pop('locations', [])
        names = kwargs.pop('names', [])
        expressions = []
        self.next.do_shizzle(image=image, locations=locations, names=names, expressions=expressions)