import pytest

from src.background_processes import BackGroundProcess
from src.model import DataIn, DataOut

background_process = BackGroundProcess()


@pytest.mark.asyncio
async def test_data_quality_check_valid():
    valid_data = DataIn(
        customer_id=1,
        service_id=1,
        timestamp='2024-05-05',
        review_txt='test',
        review_score=3
    )
    await background_process.check_data_quality(valid_data)
    validated_data: DataOut = background_process.queue_out.get_nowait()
    assert validated_data.valid


@pytest.mark.asyncio
async def test_data_quality_check_not_valid_missing_field():
    invalid_data = DataIn(
        customer_id=None,
        service_id=1,
        timestamp='2024-05-05',
        review_txt='test',
        review_score=3
    )
    await background_process.check_data_quality(invalid_data)
    validated_data: DataOut = background_process.queue_out.get_nowait()
    assert not validated_data.valid


@pytest.mark.asyncio
async def test_data_quality_check_not_valid_bad_review_score():
    invalid_data = DataIn(
        customer_id=1,
        service_id=1,
        timestamp='2024-05-05',
        review_txt='test',
        review_score=6
    )
    await background_process.check_data_quality(invalid_data)
    validated_data: DataOut = background_process.queue_out.get_nowait()
    assert not validated_data.valid

