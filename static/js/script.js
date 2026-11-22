
document.addEventListener('DOMContentLoaded', function() {
    const itemSelect = document.getElementById('id_item');
    const dynamicContainer = document.getElementById('dynamic-option-container');
    const dynamicLabel = document.getElementById('dynamic-label');
    const dynamicSelect = document.getElementById('specific_option');

    if (!itemSelect) return;

    itemSelect.addEventListener('change', function() {
        const selectedItem = this.value;

        dynamicSelect.innerHTML = '<option value="">-- Select Option --</option>';

        if (selectedItem === 'uniform') {
            dynamicContainer.style.display = 'block';
            dynamicContainer.classList.remove('hidden');
            dynamicLabel.innerText = 'Select Size';
            addOptions(['Small', 'Medium', 'Large', 'Extra Large']);
        } 
        else if (selectedItem === 'sling') {
            dynamicContainer.style.display = 'block';
            dynamicContainer.classList.remove('hidden');
            dynamicLabel.innerText = 'Select Sling Color';
            addOptions(['Royal Blue', 'Royal Red']);
        } 
        else if (selectedItem === 'cover') {
            dynamicContainer.style.display = 'block';
            dynamicContainer.classList.remove('hidden');
            dynamicLabel.innerText = 'Select Cover Type';
            addOptions(['Hard Case', 'Soft Silicone']);
        } 
        else {
            dynamicContainer.style.display = 'none';
            dynamicContainer.classList.add('hidden');
        }
    });

    function addOptions(optionsArray) {
        optionsArray.forEach(opt => {
            let el = document.createElement('option');
            el.textContent = opt;
            el.value = opt.toLowerCase().replace(/\s+/g, '_');
            dynamicSelect.appendChild(el);
        });
    }

    const resetBtn = document.querySelector('.btn-reset');
    if (resetBtn) {
        resetBtn.addEventListener('click', function(e) {
            e.preventDefault();
            document.getElementById('orderForm').reset();
            dynamicContainer.style.display = 'none';
            dynamicContainer.classList.add('hidden');
        });
    }
});
