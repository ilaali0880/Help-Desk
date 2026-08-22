document.addEventListener('DOMContentLoaded', function () {

    /* ---------- ۱. Fade-in برای container و کارت‌ها ---------- */
    const container = document.querySelector('.container');
    if (container) {
        container.classList.add('fade-in');
    }

    document.querySelectorAll('.ticket-item, .stat-card, .comment-box').forEach(function (el, index) {
        el.style.animationDelay = (index * 0.06) + 's';
        el.classList.add('fade-in-item');
    });


    /* ---------- ۲. تأیید قبل از بستن تیکت ---------- */
    const statusForm = document.querySelector('form button[name="status_submit"]');
    if (statusForm) {
        const statusSelect = document.querySelector('#id_status');
        statusForm.closest('form').addEventListener('submit', function (e) {
            if (statusSelect && statusSelect.value === 'C') {
                const confirmed = confirm('آیا مطمئنی می‌خوای این تیکت رو ببندی؟');
                if (!confirmed) {
                    e.preventDefault();
                }
            }
        });
    }


    /* ---------- ۳. شمارشگر کاراکتر برای description و message ---------- */
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(function (textarea) {
        const counter = document.createElement('div');
        counter.className = 'char-counter';
        counter.textContent = textarea.value.length + ' کاراکتر';
        textarea.insertAdjacentElement('afterend', counter);

        textarea.addEventListener('input', function () {
            counter.textContent = textarea.value.length + ' کاراکتر';
        });
    });


    /* ---------- ۴. جستجوی زنده (بدون رفرش کامل صفحه) ---------- */
    const filterForm = document.querySelector('.filter-form');
    if (filterForm) {
        const searchInput = filterForm.querySelector('input[name="q"]');
        const statusSelectFilter = filterForm.querySelector('select[name="status"]');
        const resultsWrapper = document.querySelector('#ticket-results');

        let debounceTimer;

        function runLiveFilter() {
            const params = new URLSearchParams();
            if (searchInput.value) params.set('q', searchInput.value);
            if (statusSelectFilter.value) params.set('status', statusSelectFilter.value);

            fetch(window.location.pathname + '?' + params.toString() + '&ajax=1')
                .then(function (response) { return response.text(); })
                .then(function (html) {
                    resultsWrapper.innerHTML = html;
                    window.history.replaceState(null, '', '?' + params.toString());

                    resultsWrapper.querySelectorAll('.ticket-item').forEach(function (el, index) {
                        el.style.animationDelay = (index * 0.06) + 's';
                        el.classList.add('fade-in-item');
                    });
                });
        }

        searchInput.addEventListener('input', function () {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(runLiveFilter, 400);
        });

        statusSelectFilter.addEventListener('change', runLiveFilter);

        filterForm.addEventListener('submit', function (e) {
            e.preventDefault();
            runLiveFilter();
        });
    }


    /* ---------- ۵. انیمیشن شمارش اعداد در داشبورد ---------- */
    document.querySelectorAll('.stat-number').forEach(function (el) {
        const target = parseInt(el.textContent, 10);
        if (isNaN(target)) return;

        let current = 0;
        const duration = 800;
        const stepTime = Math.max(Math.floor(duration / Math.max(target, 1)), 20);

        el.textContent = '0';

        const timer = setInterval(function () {
            current++;
            el.textContent = current;
            if (current >= target) {
                clearInterval(timer);
            }
        }, stepTime);
    });

});