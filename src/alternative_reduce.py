#!/usr/bin/env python3

# command line args
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '--hashtags',
    nargs='+',
    required=True,
    help='hashtags to plot, e.g. "#coronavirus" "#covid19"'
)
parser.add_argument(
    '--input_folder',
    default='outputs'
)
parser.add_argument(
    '--output_path',
    default='alternative_reduce.png'
)
args = parser.parse_args()


# imports
import os
import glob
import json
import datetime
import matplotlib.pyplot as plt


# support Korean text
plt.rcParams['font.family'] = 'UnDotum'


# initialize:
#
# data['#coronavirus'][32] = number of #coronavirus tweets
#                           on day 32 of 2020
data = {
    hashtag: {}
    for hashtag in args.hashtags
}


# scan all daily language mapper outputs
paths = glob.glob(os.path.join(args.input_folder, '*.lang'))

for path in paths:

    # filename looks like:
    # geoTwitter20-01-01.zip.lang
    basename = os.path.basename(path)

    date_string = basename[
        len('geoTwitter') :
        len('geoTwitter') + 8
    ]

    # converts 20-01-01 -> datetime
    date = datetime.datetime.strptime(date_string, '%y-%m-%d')

    # convert date to day of year: Jan 1 = 1
    day_of_year = date.timetuple().tm_yday

    # load this day's mapper output
    with open(path) as f:
        counts = json.load(f)

    # calculate daily total for each requested hashtag
    for hashtag in args.hashtags:

        # counts[hashtag] contains counts by language
        #
        # e.g.
        # {
        #     "en": 500,
        #     "es": 40,
        #     "fr": 20
        # }
        #
        # summing gives total tweets containing that hashtag
        daily_total = sum(
            counts.get(hashtag, {}).values()
        )

        data[hashtag][day_of_year] = daily_total


# plot
plt.figure(figsize=(12, 6))

for hashtag in args.hashtags:

    # include all 366 days, even if a day has zero matches
    days = list(range(1, 367))
    values = [
        data[hashtag].get(day, 0)
        for day in days
    ]

    plt.plot(
        days,
        values,
        label=hashtag,
        linewidth=1.5
    )


plt.xlabel('Day of year (2020)')
plt.ylabel('Number of tweets')
plt.title('Hashtag usage on Twitter during 2020')

plt.xlim(1, 366)
plt.grid(alpha=0.25)
plt.legend()

plt.tight_layout()
plt.savefig(args.output_path, dpi=150)
plt.close()

print('saving', args.output_path)
