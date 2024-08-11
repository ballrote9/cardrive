document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded event triggered');

    var filterPanel = document.getElementById("filter-panel");
    var btn = document.getElementById("filter-btn");
    var closeBtn = document.getElementsByClassName("close-filter-panel")[0];
    var main = document.getElementById('main-content');

    console.log('filterPanel:', filterPanel);
    console.log('btn:', btn);
    console.log('closeBtn:', closeBtn);

    if (!filterPanel || !btn || !closeBtn) {
        console.error('One or more elements are missing.');
        return;
    }

    var priceMinInput = document.getElementById("price-min");
    var priceMaxInput = document.getElementById("price-max");
    var priceRangeMin = document.getElementById("price-range-min");
    var priceRangeMax = document.getElementById("price-range-max");

    btn.onclick = function() {
        console.log('Filter button clicked');
        if (filterPanel.style.display === "block") {
            filterPanel.style.display = "none";
            filterPanel.style.maxHeight = "0";
            main.style.marginTop = '80px';
        } else {
            filterPanel.style.display = "block";
            filterPanel.style.maxHeight = filterPanel.scrollHeight + "px";
            main.style.marginTop = '-25px';
        }
    }

    closeBtn.onclick = function() {
        filterPanel.style.display = "none";
        filterPanel.style.maxHeight = "0";
        main.style.marginTop = '80px';
    }

    window.onclick = function(event) {
        if (event.target == filterPanel) {
            filterPanel.style.display = "none";
            filterPanel.style.maxHeight = "0";
        }
    }

    priceRangeMin.oninput = function() {
        priceMinInput.value = priceRangeMin.value;
    }

    priceRangeMax.oninput = function() {
        priceMaxInput.value = priceRangeMax.value;
    }

    priceMinInput.oninput = function() {
        priceRangeMin.value = priceMinInput.value;
    }

    priceMaxInput.oninput = function() {
        priceRangeMax.value = priceMaxInput.value;
    }
});
