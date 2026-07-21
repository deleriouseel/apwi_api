"""
Seed the station / location / airtime tables from the data that used to be
hardcoded in the frontend (apwi_front src/components/Stations.jsx).

Run once against the database the API is configured for (see app/.env):

    python seed_stations.py            # insert missing rows
    python seed_stations.py --dry-run  # show what would happen, change nothing

Location codes follow ISO 3166:
  - country : ISO 3166-1 alpha-2  ("US", "UG")
  - state   : ISO 3166-2          ("US-WA", "US-CA"); empty when none applies

The script is idempotent: airtimes and locations are get-or-created, and a
station is matched by (name, frequency) so re-running does not duplicate data.
It only ADDS rows; it never deletes. Existing rows are left untouched.
"""

import argparse
import datetime
import sys

from app.database import SessionLocal
from app import models


# All current listings air on weekdays, so airdays is "weekdays" throughout.
AIRDAYS = "weekdays"


def get_or_create_airtime(db, hour, minute):
    t = datetime.time(hour, minute)
    obj = (
        db.query(models.AIRTIME)
        .filter(models.AIRTIME.time == t, models.AIRTIME.airdays == AIRDAYS)
        .first()
    )
    if obj:
        return obj
    obj = models.AIRTIME(time=t, airdays=AIRDAYS)
    db.add(obj)
    db.flush()  # assign idAirtime without committing
    return obj


def get_or_create_location(db, city, state, country):
    obj = (
        db.query(models.LOCATION)
        .filter(
            models.LOCATION.city == city,
            models.LOCATION.state == state,
            models.LOCATION.country == country,
        )
        .first()
    )
    if obj:
        return obj
    obj = models.LOCATION(city=city, state=state, country=country)
    db.add(obj)
    db.flush()
    return obj


def get_or_create_station(db, name, frequency, network, callletters, local,
                          location, airtimes):
    """Match a station by (name, frequency) so re-runs don't duplicate it."""
    station = (
        db.query(models.STATION)
        .filter(models.STATION.name == name, models.STATION.frequency == frequency)
        .first()
    )
    created = False
    if not station:
        station = models.STATION(
            name=name,
            frequency=frequency,
            network=network,
            callletters=callletters,
            live=False,
            local=local,
        )
        db.add(station)
        db.flush()
        created = True
    else:
        # Keep the local flag in sync on re-runs.
        station.local = local

    # Link location and airtimes idempotently (avoid duplicate junction rows).
    if location not in station.locations:
        station.locations.append(location)
    for at in airtimes:
        if at not in station.airtimes:
            station.airtimes.append(at)

    return station, created


# --- The data ------------------------------------------------------------------
# Each entry:
#   name        : display name (call letters or region)
#   frequency   : e.g. "630 AM", "88.1 FM"
#   callletters : e.g. "KTRW" or None when the listing has no call sign
#   network     : "ACN" or "CALVARY"
#   city        : city / region label
#   state       : ISO 3166-2 subdivision code ("US-WA"), or "" if none
#   country     : ISO 3166-1 alpha-2 ("US", "UG")
#   times       : list of (hour, minute) 24h tuples this station airs at
#
# Extracted from the active (non-commented) entries in Stations.jsx.
STATIONS = [
    # --- Local: Spokane / North Idaho ---
    dict(name="KTRW", frequency="630 AM", callletters="KTRW", network="ACN",
         city="Spokane", state="US-WA", country="US", times=[(12, 0), (17, 30)]),
    dict(name="KTRW", frequency="96.5 FM", callletters="KTRW", network="ACN",
         city="Spokane", state="US-WA", country="US", times=[(12, 0), (17, 30)]),
    dict(name="KTWD", frequency="103.5 FM", callletters="KTWD", network="CALVARY",
         city="Wallace", state="US-ID", country="US", times=[(7, 0), (10, 0)]),

    # --- California (Calvary) ---
    dict(name="KRTM", frequency="88.1 FM", callletters="KRTM", network="CALVARY",
         city="Banning", state="US-CA", country="US", times=[(7, 0), (10, 0)]),
    dict(name="Fallbrook", frequency="106.7 FM", callletters=None, network="CALVARY",
         city="Fallbrook", state="US-CA", country="US", times=[(7, 0), (10, 0)]),
    dict(name="Hemet", frequency="97.9 FM", callletters=None, network="CALVARY",
         city="Hemet", state="US-CA", country="US", times=[(7, 0), (10, 0)]),
    dict(name="KGDM", frequency="105.3 FM", callletters="KGDM", network="CALVARY",
         city="Merced", state="US-CA", country="US", times=[(7, 0)]),
    dict(name="KDIA", frequency="1640 AM", callletters="KDIA", network="CALVARY",
         city="San Francisco", state="US-CA", country="US", times=[(7, 30)]),

    # --- Florida (Calvary) ---
    dict(name="Gainesville", frequency="94.7 FM", callletters=None, network="CALVARY",
         city="Gainesville", state="US-FL", country="US", times=[]),  # "Weekdays", no time given

    # --- Idaho (Calvary) ---
    dict(name="Grangeville", frequency="90.5 FM", callletters=None, network="CALVARY",
         city="Grangeville", state="US-ID", country="US", times=[(5, 30)]),
    dict(name="Moscow/Pullman", frequency="103.5 FM", callletters=None, network="CALVARY",
         city="Moscow/Pullman", state="US-ID", country="US", times=[(5, 30)]),
    dict(name="Meridian", frequency="97.5 FM", callletters=None, network="CALVARY",
         city="Meridian", state="US-ID", country="US", times=[(6, 30)]),

    # --- Missouri (Calvary) ---
    dict(name="Bethany", frequency="91.3 FM", callletters=None, network="CALVARY",
         city="Bethany", state="US-MO", country="US", times=[(7, 0), (10, 0)]),

    # --- New Jersey (Calvary) ---
    dict(name="Monmouth, Ocean County", frequency="89.7 FM", callletters=None, network="CALVARY",
         city="Monmouth, Ocean County", state="US-NJ", country="US", times=[(4, 30)]),
    dict(name="Southern Middlesex, Northern Monmouth County", frequency="91.9 FM", callletters=None,
         network="CALVARY", city="Southern Middlesex, Northern Monmouth County", state="US-NJ",
         country="US", times=[(4, 30)]),
    dict(name="Northern Jersey", frequency="103.1 FM", callletters=None, network="CALVARY",
         city="Northern Jersey", state="US-NJ", country="US", times=[(4, 30)]),

    # --- New York (Calvary) ---
    dict(name="New York City", frequency="95.1 FM", callletters=None, network="CALVARY",
         city="New York City", state="US-NY", country="US", times=[(4, 30)]),
    dict(name="Sullivan, Orange County", frequency="99.7 FM", callletters=None, network="CALVARY",
         city="Sullivan, Orange County", state="US-NY", country="US", times=[(4, 30)]),
    dict(name="Poughkeepsie", frequency="106.9 FM", callletters=None, network="CALVARY",
         city="Poughkeepsie", state="US-NY", country="US", times=[(4, 30)]),

    # --- Texas (Calvary) ---
    dict(name="KYJC", frequency="91.3 FM", callletters="KYJC", network="CALVARY",
         city="Commerce", state="US-TX", country="US", times=[(7, 0), (10, 0)]),
    dict(name="Dallas/Fort Worth", frequency="97.5 FM", callletters=None, network="CALVARY",
         city="Dallas/Fort Worth", state="US-TX", country="US", times=[(7, 0), (10, 0)]),
    dict(name="KDKR", frequency="91.3 FM", callletters="KDKR", network="CALVARY",
         city="Dallas/Fort Worth", state="US-TX", country="US", times=[(7, 0), (10, 0)]),
    dict(name="Irving", frequency="99.9 FM", callletters=None, network="CALVARY",
         city="Irving", state="US-TX", country="US", times=[(7, 0), (10, 0)]),

    # --- Washington (ACN) ---
    dict(name="KTBI", frequency="810 AM", callletters="KTBI", network="ACN",
         city="Wenatchee", state="US-WA", country="US", times=[(7, 0), (17, 30), (23, 0)]),
    dict(name="KYAK", frequency="930 AM", callletters="KYAK", network="ACN",
         city="Yakima", state="US-WA", country="US", times=[(7, 0), (17, 30), (23, 0)]),

    # --- Washington (Calvary) ---
    dict(name="Pullman/Moscow", frequency="103.5 FM", callletters=None, network="CALVARY",
         city="Pullman/Moscow", state="US-WA", country="US", times=[(5, 30)]),

    # --- Uganda (Calvary) ---
    dict(name="Kampala", frequency="92.7 FM", callletters=None, network="CALVARY",
         city="Kampala", state="", country="UG", times=[(10, 0)]),
]


def main():
    parser = argparse.ArgumentParser(description="Seed station data.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Report what would happen without writing.")
    args = parser.parse_args()

    db = SessionLocal()
    created_count = 0
    linked_count = 0
    try:
        for row in STATIONS:
            location = get_or_create_location(
                db, row["city"], row["state"], row["country"]
            )
            airtimes = [get_or_create_airtime(db, h, m) for (h, m) in row["times"]]
            # Local = the Spokane / North Idaho area: Spokane (KTRW) and
            # Wallace (KTWD). New stations can be marked local directly in the
            # DB (station.local) without editing this rule.
            is_local = row["city"] in ("Spokane", "Wallace")
            station, created = get_or_create_station(
                db,
                name=row["name"],
                frequency=row["frequency"],
                network=row["network"],
                callletters=row["callletters"],
                local=is_local,
                location=location,
                airtimes=airtimes,
            )
            if created:
                created_count += 1
                print(f"  + {row['network']:8} {row['name']} {row['frequency']} "
                      f"({row['city']}, {row['state'] or row['country']})")
            else:
                linked_count += 1
                print(f"  = exists: {row['name']} {row['frequency']} (links ensured)")

        if args.dry_run:
            db.rollback()
            print(f"\nDRY RUN — rolled back. Would create {created_count} stations.")
        else:
            db.commit()
            print(f"\nDone. Created {created_count} new stations, "
                  f"{linked_count} already existed.")
    except Exception:
        db.rollback()
        print("\nError — rolled back, no changes made.", file=sys.stderr)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
