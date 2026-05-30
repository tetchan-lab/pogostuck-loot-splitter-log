# Pogostuck Loot Mode Auto-Splitter (Log-based)

An auto-splitter for Pogostuck **Loot Mode** that works with LiveSplit, automatically splitting on each floor transition.

Instead of screen capture or OCR, this tool monitors the game's log file (`acklog.txt`) directly — making it **lightweight and accurate**.

---

## Features

- **No screen capture or OCR** — extremely lightweight
- **No false detections** — reads directly from the game engine log
- **No additional libraries required** — uses Python standard library only
- Automatically splits on each floor clear
- Automatically resets and restarts the timer when a new run begins

---

## Requirements

| Software | Download |
|---|---|
| Python 3.10 or later | https://www.python.org/downloads/ |
| LiveSplit | https://livesplit.org/ |
| Pogostuck (launch option required) | Steam |

---

## Download

### Without Git (recommended)

1. Click the green **`Code`** button at the top right of this page
2. Select **`Download ZIP`**
3. Extract the ZIP and place the folder wherever you like (e.g. `C:\tools\pogostuck-loot-splitter-log\`)

### With Git

```
git clone https://github.com/tetchan-lab/pogostuck-loot-splitter-log.git
```

---

## Installing Python

### 1. Download Python

1. Go to https://www.python.org/downloads/
2. Click the **`Download Python 3.x.x`** button to download the installer

### 2. Install Python

1. Run the downloaded `.exe` file
2. **⚠️ Important:** Check **`Add python.exe to PATH`** at the bottom of the installer screen
3. Click **`Install Now`**

> If you forget to check `Add python.exe to PATH`, the `start_autosplitter.bat` file will not work. To fix this, re-run the installer, select `Modify` → `Next`, and check `Add Python to environment variables`.

### 3. Verify the installation

Open PowerShell from the Start menu and run:

```
python --version
```

If you see `Python 3.x.x`, the installation was successful.

---

## Setup

### 1. Set Pogostuck launch options

In your Steam library, right-click Pogostuck → `Properties` → `Launch Options` and enter:

```
-diag
```

> The `-diag` option enables log output to `acklog.txt`. Without it, this tool will not work.

### 2. Configure LiveSplit

LiveSplit has a built-in TCP Server feature. Use one of the following methods to start it:

**Start manually each time:**
1. Launch LiveSplit
2. Right-click the window → `Control` → `Start TCP Server`

**Start automatically on launch (recommended):**
1. Right-click LiveSplit → `Settings`
2. Under `Startup Behavior`, select `Start TCP Server`
3. LiveSplit will now start the TCP Server automatically on launch

> Leave the port at the default value of `16834`.

### 3. Configure LiveSplit splits

Open `Edit Splits` and create a segment for each floor:

| Segment name (example) | When it triggers |
|---|---|
| Floor 1 | On clearing Level 1 |
| Floor 2 | On clearing Level 2 |
| Floor 3 | On clearing Level 3 |
| ... (add as many as needed) | |

### 4. Start the script

Double-click `start_autosplitter.bat`.

```
Launch game → Select Loot Mode → Timer starts automatically!
```

---

## File Structure

```
pogostuck-loot-splitter-log/
├── autosplitter.py              # Main script
├── start_autosplitter.bat       # Normal launch (double-click this)
├── start_autosplitter_test.bat  # Test mode (no LiveSplit commands sent)
└── README.md                    # This file (Japanese)
└── README.en.md                 # English version
```

---

## Test Mode

Running `start_autosplitter_test.bat` prints output to the console without sending any commands to LiveSplit. Useful for verifying behavior and troubleshooting.

```
[New run detected] seed=7877
  [TEST] LiveSplit: [reset]
  [TEST] LiveSplit: [starttimer]

[Floor 1 → Floor 2] → split
  [TEST] LiveSplit: [split]
```

---

## How It Works

The tool monitors `acklog.txt` every 0.3 seconds and detects the following patterns:

| Detection | Command sent to LiveSplit |
|---|---|
| New run started (seed value updated) | `reset` → `starttimer` |
| Advanced to next floor | `split` |
| Game restarted | Internal state reset (waits for next run) |

---

## Troubleshooting

**Timer doesn't start**
- Make sure the LiveSplit TCP Server is running (`Start TCP Server`)
- Make sure `-diag` is in your Pogostuck launch options

**Floors clear but no split happens**
- Run `start_autosplitter_test.bat` in test mode and check if `[Floor N → Floor N+1]` appears in the console

**Error saying `acklog.txt` not found**
- Launch Pogostuck at least once before running this script

---

## Related Projects

- [pogostuck-loot-splitter-ocr](https://github.com/tetchan-lab/pogostuck-loot-splitter-ocr) — OCR-based version using screen capture. Also supports score display.

---

## License

MIT License
