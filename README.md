# Install

1. Make sure you have Python3 and Pip installed
1. Clone or download this repo to your computer
1. Install packages: `pip install -r requirements.txt`
1. Configure the scraper config by editing the `.env` file
1. Run script based on config file:  `python scraper.py`

---

# Config

Create a file named `.env` to configure the scraper before running the script.

## Parameters

Please follow the constraints listed below in order to avoid bugs or crashes.

| Parameter           | Type | Example                    |
|---------------------|------|----------------------------|
| `HELIUM_HOTSPOTS`   | List | `["hotspot1", "hotspot2"]` |
| `HELIUM_DATE_START` | Date | `YYYY-MM-DD`               |
| `HELIUM_DATE_END`   | Date | `YYYY-MM-DD`               |

## Example

```py
HELIUM_HOTSPOTS='["112JaSahbeGycRr9dAzJALckxq7gxEewvhf8hBitWmiu6kbcdGPC", "112DcZEZFVomTmuqjbW2axozVAtwXQqAUereenqfECUNqEL3CqpL"]'
HELIUM_DATE_START="2021-12-20"
HELIUM_DATE_END="2021-12-31"
```