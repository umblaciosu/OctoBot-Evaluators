# cython: language_level=3
#  Drakkar-Software OctoBot-Evaluators
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.

from octobot_channels.channels.channel import Channel
from octobot_channels.constants import CHANNEL_WILDCARD
from octobot_channels.consumer import Consumer
from octobot_channels.producer import Producer
from octobot_commons.logging.logging_util import get_logger


class EvaluatorsChannelConsumer(Consumer):
    pass


class EvaluatorsChannelProducer(Producer):
    # noinspection PyMethodOverriding
    async def send(self,
                   matrix_id,
                   data,
                   evaluator_name=CHANNEL_WILDCARD,
                   evaluator_type=CHANNEL_WILDCARD,
                   exchange_name=CHANNEL_WILDCARD,
                   cryptocurrency=CHANNEL_WILDCARD,
                   symbol=CHANNEL_WILDCARD,
                   time_frame=CHANNEL_WILDCARD):
        for consumer in self.channel.get_filtered_consumers(matrix_id=matrix_id,
                                                            data=data,
                                                            evaluator_name=evaluator_name,
                                                            evaluator_type=evaluator_type,
                                                            exchange_name=exchange_name,
                                                            cryptocurrency=cryptocurrency,
                                                            symbol=symbol,
                                                            time_frame=time_frame):
            await consumer.queue.put({
                "matrix_id": matrix_id,
                "evaluator_name": evaluator_name,
                "evaluator_type": evaluator_type,
                "exchange_name": exchange_name,
                "cryptocurrency": cryptocurrency,
                "symbol": symbol,
                "time_frame": time_frame,
                "data": data
            })


class EvaluatorsChannel(Channel):
    PRODUCER_CLASS = EvaluatorsChannelProducer
    CONSUMER_CLASS = EvaluatorsChannelConsumer

    MATRIX_ID_KEY = "matrix_id"
    EVALUATOR_NAME_KEY = "evaluator_name"
    EVALUATOR_TYPE_KEY = "evaluator_type"
    EXCHANGE_NAME_KEY = "exchange_name"
    CRYPTOCURRENCY_KEY = "cryptocurrency"
    SYMBOL_KEY = "symbol"
    TIME_FRAME_KEY = "time_frame"

    def __init__(self):
        super().__init__()
        self.logger = get_logger(f"{self.__class__.__name__}")

    # noinspection PyMethodOverriding
    async def new_consumer(self,
                           callback: object,
                           size=0,
                           matrix_id=CHANNEL_WILDCARD,
                           evaluator_name=CHANNEL_WILDCARD,
                           evaluator_type=CHANNEL_WILDCARD,
                           exchange_name=CHANNEL_WILDCARD,
                           cryptocurrency=CHANNEL_WILDCARD,
                           symbol=CHANNEL_WILDCARD,
                           time_frame=CHANNEL_WILDCARD):
        consumer = EvaluatorsChannelConsumer(callback, size=size)
        await self._add_new_consumer_and_run(consumer,
                                             matrix_id=matrix_id,
                                             evaluator_name=evaluator_name,
                                             evaluator_type=evaluator_type,
                                             exchange_name=exchange_name,
                                             cryptocurrency=cryptocurrency,
                                             symbol=symbol,
                                             time_frame=time_frame)
        return consumer

    def get_filtered_consumers(self,
                               matrix_id=CHANNEL_WILDCARD,
                               evaluator_name=CHANNEL_WILDCARD,
                               evaluator_type=CHANNEL_WILDCARD,
                               exchange_name=CHANNEL_WILDCARD,
                               cryptocurrency=CHANNEL_WILDCARD,
                               symbol=CHANNEL_WILDCARD,
                               time_frame=CHANNEL_WILDCARD):
        return self.get_consumer_from_filters({
            self.MATRIX_ID_KEY: matrix_id,
            self.EVALUATOR_NAME_KEY: evaluator_name,
            self.EVALUATOR_TYPE_KEY: evaluator_type,
            self.EXCHANGE_NAME_KEY: exchange_name,
            self.CRYPTOCURRENCY_KEY: cryptocurrency,
            self.SYMBOL_KEY: symbol,
            self.TIME_FRAME_KEY: time_frame,
        })

    async def _add_new_consumer_and_run(self, consumer,
                                        matrix_id=CHANNEL_WILDCARD,
                                        evaluator_name=CHANNEL_WILDCARD,
                                        evaluator_type=CHANNEL_WILDCARD,
                                        exchange_name=CHANNEL_WILDCARD,
                                        cryptocurrency=CHANNEL_WILDCARD,
                                        symbol=CHANNEL_WILDCARD,
                                        time_frame=CHANNEL_WILDCARD):
        consumer_filters: dict = {
            self.MATRIX_ID_KEY: matrix_id,
            self.EVALUATOR_NAME_KEY: evaluator_name,
            self.EVALUATOR_TYPE_KEY: evaluator_type,
            self.EXCHANGE_NAME_KEY: exchange_name,
            self.CRYPTOCURRENCY_KEY: cryptocurrency,
            self.SYMBOL_KEY: symbol,
            self.TIME_FRAME_KEY: time_frame
        }

        self.add_new_consumer(consumer, consumer_filters)
        await consumer.run()