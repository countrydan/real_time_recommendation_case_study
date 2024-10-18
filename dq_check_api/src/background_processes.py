from asyncio import Queue

from src.model import DataIn, DataOut


class BackGroundProcess:
    REVIEW_SCORES = (1, 2, 3, 4, 5)

    def __init__(self):
        self.queue_in: Queue[DataIn] = Queue()
        self.queue_out: Queue[DataOut] = Queue()

    async def process_queue_in(self):
        """Gets a record from the queue in and does the data quality check."""
        while True:
            record = await self.queue_in.get()
            await self.check_data_quality(record)

    async def check_data_quality(self, data: DataIn):
        """
        This function first checks for missing values and then if the review score is in the valid range.
        If any of these are violated a valid flag is set to false, otherwise to true.
        Finally, the validated record is put into the queue out.

        :param data: Json received
        """
        valid = True
        if not all(data.model_dump().values()):
            valid = False
        if data.review_score not in self.REVIEW_SCORES:
            valid = False
        await self.queue_out.put(DataOut(**data.model_dump(), valid=valid))
        print('dq done')

    async def send_from_queue_out(self):
        """Send validated data to other services or channels."""
        while True:
            print('sending')
            record = await self.queue_out.get()
            # send record to Kafka or other service
