# What is this?

This is a simple script that scrapes Helium's API and CoinGecko's API in order to create a structured excel earnings report for a particular hotspot. The script can be used to create reports for one or more hotspots at the same time, and it provides the actual HNT value earned plus the current market value in USD at the earning time. Moreover, this might serve as a great learning resource into making requests.

# Contribute

Feel free to fork this script and modify it, or open a pull request to improve it.

If you found this script useful, please consider donating in HNT or ETH:
- `13bn79zQ6feucipPtLAm24ktDa2Ey3PA8NrBKEJw547L8Ez8Lgp` (HNT)
- `0x40186d2147347fb286d5d2aa0ee6d32384bba8c2` (ETH)

# Install

1. Make sure you have Python3 and Pip installed. You can check this using `python --version` and `pip --version`
1. Clone this repo using `git clone https://github.com/vladieboi/helium-explorer-scraper/` (or download it)
1. Install rquired packages using `pip install -r requirements.txt`
1. Configure the scraper config by creating a file named `.env` and configuring it as shown below
1. Run the script: `python scraper.py`

---

# Config

Create a file named `.env` to configure the scraper before running the script.

## Parameters (.env file)

| Parameter           | Type | Example                    |
|---------------------|------|----------------------------|
| `HELIUM_HOTSPOTS`   | List | `["hotspot1", "hotspot2"]` |
| `HELIUM_DATE_START` | Date | `YYYY-MM-DD`               |
| `HELIUM_DATE_END`   | Date | `YYYY-MM-DD`               |

## Example (.env file)

```py
HELIUM_HOTSPOTS='["112Ny4N65CVXAL1VfB42mtV6LvxiPWVUvReiJAr3v6r9fcrfnuSW", "112RWvXLnSb6Wtmw4Ftxi5CW29k2C4axdwTYGq8LkJrhrr8DcUWB"]'
HELIUM_DATE_START="2021-12-20"
HELIUM_DATE_END="2021-12-31"
```
