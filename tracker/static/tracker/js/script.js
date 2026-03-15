document.addEventListener('DOMContentLoaded', function () {
    const filterForm = document.querySelector('.filter-form');
    const categoryField = document.getElementById('category');
    const typeField = document.getElementById('type');
    const dateFromField = document.getElementById('date_from');
    const dateToField = document.getElementById('date_to');
    const dateWarning = document.getElementById('date-warning');

    const balanceValue = document.getElementById('balance-value');
    const budgetCard = document.getElementById('budget-card');

    if (filterForm && categoryField) {
        categoryField.addEventListener('change', function () {
            filterForm.submit();
        });
    }

    if (filterForm && typeField) {
        typeField.addEventListener('change', function () {
            filterForm.submit();
        });
    }

    function validateDates() {
        if (!dateFromField || !dateToField || !dateWarning) {
            return true;
        }

        const dateFrom = dateFromField.value;
        const dateTo = dateToField.value;

        if (dateFrom && dateTo && dateFrom > dateTo) {
            dateWarning.style.display = 'block';
            return false;
        }

        dateWarning.style.display = 'none';
        return true;
    }

    if (dateFromField) {
        dateFromField.addEventListener('change', function () {
            if (validateDates() && filterForm && dateToField && dateToField.value) {
                filterForm.submit();
            }
        });
    }

    if (dateToField) {
        dateToField.addEventListener('change', function () {
            if (validateDates() && filterForm && dateFromField && dateFromField.value) {
                filterForm.submit();
            }
        });
    }

    if (balanceValue) {
        const balance = parseFloat(balanceValue.dataset.value);
        if (!isNaN(balance) && balance < 0) {
            balanceValue.classList.add('text-danger', 'fw-bold');
        }
    }

    if (budgetCard) {
        const status = budgetCard.dataset.budgetStatus;

        if (status === 'warning') {
            budgetCard.classList.add('border', 'border-warning');
        } else if (status === 'exceeded') {
            budgetCard.classList.add('border', 'border-danger');
        } else if (status === 'safe') {
            budgetCard.classList.add('border', 'border-success');
        }
    }
});