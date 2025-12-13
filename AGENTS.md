# Repository Guidelines

## Project Structure & Module Organization
- `main.py`: client entry point initializing Pygame scenes and networking.
- `server.py` and `Server/`: headless server bootstrap plus lobby/room/user logic in `Server/Modules`.
- `content/`: game logic (`game_modules`), scenes/UI, ships, maps, and game assets references; `content/maps` holds map JSONs.
- `assets/`: textures, sounds, and other static files loaded by content modules.
- `settings/`: configuration presets (`settings.json`, `_local`, `_sakura`) and loader in `all_settings.py`.
- `requirements.txt`, `joysticktest.py`, `test.py`: dependencies and small utilities for device/network checks.

## Build, Test, and Development Commands
- Install deps: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.
- Run client: `python main.py [--debug] [--nogui]`; `--nogui` keeps networking without UI.
- Run dedicated server: `python server.py [--debug]`; uses dummy video/audio drivers for headless hosts.
- Quick joystick check: `python joysticktest.py`.
- Lint/format (recommended): `python -m compileall .` to catch syntax issues; prefer `ruff`/`black` locally if available.

## Coding Style & Naming Conventions
- Python 3, 4-space indentation; follow PEP 8 where practical.
- Use descriptive module/class names mirroring game concepts (e.g., `ScenePlayer`, `Ship`); keep file names lower_snake_case.
- Keep settings keys stable; new options belong in `settings/all_settings.py` and corresponding JSON presets.
- Favor small helpers in `content/game_modules` over duplicating logic in scenes.

## Testing Guidelines
- No formal test suite; smoke-test networking with `test.py` (adjust IP/port) and playtest core flows after changes to scenes, ships, or maps.
- When adding gameplay features, validate map loading (`content/maps`) and settings parsing; log errors via existing `Flogger` hooks.
- Document manual test steps in PRs (e.g., host server locally, connect two clients, fire weapons, verify gravity wells).

## Commit & Pull Request Guidelines
- Use short, imperative commit subjects (e.g., `Fix UDP heartbeat timeout`, `Add new asteroid map layout`); include issue IDs when applicable.
- In PRs, describe gameplay impact, config changes, and any map/asset updates; attach screenshots or short clips for UI/scene changes.
- Call out breaking protocol changes between client/server and any new required settings keys.

## Security & Configuration Tips
- Do not commit real IPs, credentials, or AES keys; use the placeholder presets in `settings/*.json` and document overrides privately.
- When testing headless, ensure dummy SDL drivers in `server.py` stay intact; avoid removing them for remote deploys.
