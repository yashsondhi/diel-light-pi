---
title: Settings
nav_order: 99
last_modified_date: 2026-09-01 14:56:20 +0000
---

# Settings

## Image Size

Adjust how large images appear across all pages.

<div id="img-size-control">
  🖼️ Image Size:
  <input type="range"  id="img-scale-slider" min="1" max="100" step="1" value="75" />
  <input type="number" id="img-scale-input"  min="1" max="100" step="1" value="75" />
  <span>%</span>
</div>

<script>
  var STORAGE_KEY = "imgScale";
  var MIN         = 1;
  var MAX         = 100;
  var DEFAULT     = 75;

  var slider = document.getElementById("img-scale-slider");
  var input  = document.getElementById("img-scale-input");

  function applyImgScale(value) {
    value = parseInt(value);
    if (isNaN(value)) value = DEFAULT;
    if (value < MIN)  value = MIN;
    if (value > MAX)  value = MAX;
    document.documentElement.style.setProperty("--img-scale", value + "%");
    slider.value = value;
    input.value  = value;
    localStorage.setItem(STORAGE_KEY, value);
  }

  var saved = localStorage.getItem(STORAGE_KEY);
  applyImgScale(saved !== null ? saved : DEFAULT);

  slider.addEventListener("input", function () {
    applyImgScale(this.value);
  });

  input.addEventListener("input", function () {
    applyImgScale(this.value);
  });
</script>
