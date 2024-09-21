

class Task:
    def __init__(self, create_time, start_time, cards, duration, gpu_time):
        self.create_time = create_time
        self.start_time = start_time
        self.cards = cards
        self.gpu_time = gpu_time
        self.duration_time = duration

        #real_parameter
        self.real_start_time = None
        self.real_end_time = None
        self.queue_time = None

    @classmethod
    def create(cls, **kwargs):
        return cls(kwargs.get('create_time'), kwargs.get('start_time'), kwargs.get('cards'), kwargs.get('duration'), kwargs.get('gpu_time'))

    def __repr__(self):
        return (f"Task(create_time:{self.create_time}, start_time={self.start_time}, "
                f"cards:{self.cards},duration_time:{self.duration_time}, "
                f"gpu_time:{self.gpu_time})\n")