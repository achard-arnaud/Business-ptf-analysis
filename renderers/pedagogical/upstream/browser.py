"""Shared Chromium launcher for the optional PDF and layout QA steps."""
import os
from pathlib import Path


async def launch(playwright):
    path = os.environ.get('NICE_CHROMIUM_PATH')
    if path and not Path(path).is_file():
        raise FileNotFoundError(f'NICE_CHROMIUM_PATH does not point to Chromium: {path}')
    kwargs = {'executable_path': path} if path else {}
    return await playwright.chromium.launch(args=['--no-sandbox'], **kwargs)

