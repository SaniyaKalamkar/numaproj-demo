import pytest
import asyncio
from unittest.mock import Mock

from pynumaflow.sourcer import ReadRequest
from pynumaflow.shared.asynciter import NonBlockingIterator

from mqtt_udsource import MQTTAsyncSource


@pytest.mark.asyncio
async def test_read_handler():
    """Test reading messages from MQTT queue"""
    source = MQTTAsyncSource("localhost", 1883, "test")
    
    # Add test messages to queue
    await source.messages.put("msg1")
    await source.messages.put("msg2")
    
    # Mock output iterator
    output = NonBlockingIterator()
    
    # Read messages
    read_req = Mock(spec=ReadRequest)
    read_req.num_records = 2
    
    await source.read_handler(read_req, output)
    
    # Verify state
    assert len(source.to_ack_set) == 2
    assert source.read_idx == 2
    print("✓ test_read_handler passed")


@pytest.mark.asyncio
async def test_ack_handler():
    """Test message acknowledgment"""
    source = MQTTAsyncSource("localhost", 1883, "test")
    source.to_ack_set = {0, 1, 2}
    
    # Mock ack request
    ack_req = Mock()
    ack_req.offsets = [Mock(offset=b"0"), Mock(offset=b"1")]
    
    await source.ack_handler(ack_req)
    
    assert source.to_ack_set == {2}
    print("✓ test_ack_handler passed")


@pytest.mark.asyncio
async def test_nack_handler():
    """Test negative acknowledgment"""
    source = MQTTAsyncSource("localhost", 1883, "test")
    source.to_ack_set = {0, 1}
    
    # Mock nack request
    nack_req = Mock()
    nack_req.offsets = [Mock(offset=b"0")]
    
    await source.nack_handler(nack_req)
    
    assert 0 not in source.to_ack_set
    assert 0 in source.nacked
    print("✓ test_nack_handler passed")


@pytest.mark.asyncio
async def test_pending_handler():
    """Test pending message count"""
    source = MQTTAsyncSource("localhost", 1883, "test")
    
    await source.messages.put("msg1")
    await source.messages.put("msg2")
    
    response = await source.pending_handler()
    assert response.count == 2
    print("✓ test_pending_handler passed")


async def run_all_tests():
    """Run all tests"""
    print("Running tests...\n")
    try:
        await test_read_handler()
        await test_ack_handler()
        await test_nack_handler()
        await test_pending_handler()
        print("\n✅ All tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(run_all_tests())