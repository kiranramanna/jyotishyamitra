#!/usr/bin/env python3

import logging
logging.basicConfig(level=logging.DEBUG)

from kerykeion.astrological_subject import AstrologicalSubject
from kerykeion.charts.south_indian_chart_svg import SouthIndianChartSVG

# Create subject directly
subject = AstrologicalSubject(
    name="Vivekananda, Swami",
    year=1863,
    month=1,
    day=12,
    hour=6,
    minute=33,
    lng=88.36,
    lat=22.53,
    city="Kolkata",
    tz_str="Asia/Kolkata"
)

# Create South Indian chart
chart = SouthIndianChartSVG(subject)
svg_content = chart.makeTemplate()

print('SVG template generated successfully')

# Save to file
with open('charts/Vivekananda, Swami - South Indian Test.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)

print('Chart saved successfully')