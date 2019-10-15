class PipelineModule:

    def __init__(self, next=None):
        if next is not None and not isinstance(next, PipelineModule):
            raise ValueError("Expected argument next to be a PipelineModule or None")
        else:
            self.next = next

    def do_shizzle(self, **kwargs):
        pass