from energize.pipeline.pipeline import PipelineModule

class ReadExpressions(PipelineModule):

    def __init__(self, next=None):
        super().__init__(next)
        self.FER_model = None

    def do_shizzle(self, **kwargs):
        image = kwargs.pop('image', None)
        locations = kwargs.pop('locations', [])
        names = kwargs.pop('names', [])
        if image is not None and len(locations) > 0:
            expressions = self.get_expressions(image, locations)
        else:
            expressions = []
        self.next.do_shizzle(image=image, locations=locations, names=names, expressions=expressions)

    def get_expressions(self, image, locations):
        return ["Unknown"]*len(locations)