"""The websock integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
import websocket
import json

from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.LIGHT]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up websock from a config entry."""
    # TODO Store an API object for your platforms to access
    # hass.data[DOMAIN][entry.entry_id] = MyApi(...)

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


############# WS FUNCTIONS ####################


def on_messagews(ws, message):
    print("messaggio: "+message)

def on_errorws(ws, error):
    print(error)


def on_closews(ws, close_status_code, close_msg):
    print("Reconnecting")
    connectToBroker()


def on_openws(ws):
    ws.send(
        json.dumps({"type": "auth","access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI5NGQ4ZDMwYWMzNzQ0MDhkODM4YzZjNTY3MzFmNDhlYSIsImlhdCI6MTY1MDUzMTU5MiwiZXhwIjoxOTY1ODkxNTkyfQ.wGqiJhLJ_2YHgbuyC96iAM4K5v20L-1KYJJhVmRUCKA",})
    )  # json.dumps({"type": "auth","access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI5NGQ4ZDMwYWMzNzQ0MDhkODM4YzZjNTY3MzFmNDhlYSIsImlhdCI6MTY1MDUzMTU5MiwiZXhwIjoxOTY1ODkxNTkyfQ.wGqiJhLJ_2YHgbuyC96iAM4K5v20L-1KYJJhVmRUCKA",})
    print("Auth effettuato")
    ws.send(
        json.dumps({"id": 18, "type": "subscribe_events", "event_type": "state_changed"})
    )  # json.dumps({"id": 18, "type": "subscribe_events", "event_type": "state_changed"})
    print("Sottoscrizione agli eventi effetuata")
    print("connected")



def connectToBroker():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        "ws://192.168.3.122:8123/api/websocket",
        on_open=on_openws,
        on_message=on_messagews,
        on_error=on_errorws,
        on_close=on_closews,
    )
    ws.run_forever()