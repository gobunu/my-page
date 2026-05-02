---
layout: page
permalink: /publications/
title: publications
description: Publications grouped by year and ordered by release time.
nav: true
nav_order: 2
---

{% include bib_search.liquid %}

<p>* indicates equal contribution and † indicates corresponding author.</p>

{% include publication_year_styles.liquid %}

<div class="publications">
  {% bibliography --group_by year --sort_by sortkey --order descending %}
</div>
