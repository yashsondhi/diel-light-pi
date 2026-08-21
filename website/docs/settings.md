---
title: Settings
nav_order: 99
last_modified_date: 
---

# Settings

## Image Size

Adjust how large images appear across all pages.

<div id="img-size-control">
  🖼️ Image Size:
  <input type="range"  id="img-scale-slider" min="1" max="100" step="1" value="90" />
  <input type="number" id="img-scale-input"  min="1" max="100" step="1" value="90" />
  <span>%</span>
</div>

<script>
  var STORAGE_KEY = "imgScale";
  var DEFAULT     = 90;

  var slider = document.getElementById("img-scale-slider");
  var input  = document.getElementById("img-scale-input");

  function applyImgScale(value) {
    value = parseInt(value);
    if (isNaN(value)) value = DEFAULT;
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