"""A reloaded viewer must show the server's pause state and be able to resume it."""
import asyncio
import json
from types import SimpleNamespace

from cavesim.run import Session


def test_paused_viewer_reconnects_and_resume_reaches_other_viewers():
    class Socket:
        def __init__(self, messages=()):
            self.messages, self.sent = messages, []

        async def send(self, raw):
            self.sent.append(json.loads(raw))

        async def __aiter__(self):
            for message in self.messages:
                yield json.dumps(message)

    async def check():
        sim = SimpleNamespace(viewer_init=lambda: {"type": "init"},
                              viewer_state=lambda: {"type": "state"},
                              trails=lambda: {"type": "trails"})
        session = Session(sim, speed=1)
        session.paused = True
        observer = Socket()
        session.clients.add(observer)
        viewer = Socket([{"cmd": "viewer"}, {"cmd": "pause", "value": False}])
        await session.handler(viewer)
        await asyncio.sleep(0)  # finish the scheduled broadcasts
        assert viewer.sent[0] == {"type": "init", "paused": True}
        assert not session.paused
        assert {"type": "pause", "paused": False} in viewer.sent
        assert {"type": "pause", "paused": False} in observer.sent

    asyncio.run(check())
